from collections.abc import Iterable
from multiprocessing.pool import ThreadPool
from pycoral.utils.edgetpu import list_edge_tpus

from .cyclic_toposort import acyclic_toposort
from .input_multi_stream import InputMultiStream
from .input_stream import InputStream
from .output_stream import OutputStream
from .perceptor import Perceptor
from .perceptor_node import PerceptorNode
from .processing_engine import ProcessingEngine
from .utils import validate_not_none, validate_type


class Pipeline():
    def __init__(self, input_stream):
        validate_not_none(input_stream, "input_stream is required")
        validate_type(input_stream, (InputStream, InputMultiStream), "input_stream must be an instance of InputStream")

        self.__input_stream = input_stream
        self.__num_of_edge_tpus = len(list_edge_tpus())
        self.__perceptors = {}
        self.__output_streams = []
        self.__processing_engine = ProcessingEngine(self.__num_of_edge_tpus)
        self.__thread_pool = ThreadPool(10)

        self.__running = False


    def num_of_edge_tpus(self):
        return self.__num_of_edge_tpus


    def add_perceptor(self, name, perceptor, parent=None, multi=False, accelerator_idx=None):
        if self.__running:
            raise Exception("Pipeline is already running")

        validate_not_none(name, "name is required")
        validate_not_none(perceptor, "perceptor is required")
        validate_type(perceptor, Perceptor, "perceptor must be an instance of Perceptor")

        if accelerator_idx is not None:
            validate_type(accelerator_idx, int, "accelerator_idx must be an integer")

            if accelerator_idx >= self.__num_of_edge_tpus:
                raise ValueError("accelerator_idx must be less than %d" % self.__num_of_edge_tpus)

        if parent is not None and self.__perceptors[parent] is None:
            raise ValueError("perceptor with name '%s' does not exist" % name)

        perceptor_node = PerceptorNode(name, perceptor, multi, accelerator_idx)

        self.__perceptors[name] = perceptor_node
        if parent is not None:
            self.__perceptors[parent].add_child_perceptor(name)


    def add_output_stream(self, output_stream):
        validate_not_none(output_stream, "output_stream is required")
        validate_type(output_stream, OutputStream, "output_stream must be an instance of OutputStream")

        self.__output_streams.append(output_stream)


    def stop(self):
        self.__running = False
        self.__input_stream.stop()


    def run(self):
        self.__running = True

        try:
            stream = self.__input_stream.stream()
            validate_type(stream, Iterable, "input stream is not Iterable")

            perceptors_order = self.__get_perceptors_order()

            for input_data in stream:
                results = {}
                for perceptors in perceptors_order:
                    async_calls = [self.__thread_pool.apply_async(
                        self.__processing_engine.run,
                        args=(self.__perceptors[perceptor_name], input_data),
                        callback=self.__set_perceptor_result(results, perceptor_name)) for perceptor_name in perceptors]
                    [async_call.get() for async_call in async_calls]
        finally:
            self.__running = False


    def __set_perceptor_result(self, results, perceptor_name):
        def set_result(result):
            results[perceptor_name] = result

        return set_result


    def __get_perceptors_order(self):
        orphan_perceptors = []
        parent_perceptors = []
        visited = []

        for perceptor_name in self.__perceptors.keys():
            child_perceptors = self.__perceptors[perceptor_name].get_child_perceptors()
            if len(child_perceptors) == 0:
                if perceptor_name not in visited:
                    orphan_perceptors.append(perceptor_name)
            else:
                visited.append(perceptor_name)
                for child in child_perceptors:
                    parent_perceptors.append((perceptor_name, child))
                    visited.append(child)

        if len(parent_perceptors) > 0:
            perceptors_order = acyclic_toposort(parent_perceptors)
            [perceptors_order[0].add(x) for x in orphan_perceptors]
        else:
            perceptors_order = [{x for x in orphan_perceptors}]

        return perceptors_order
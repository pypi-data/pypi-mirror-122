from tflite_runtime.interpreter import Interpreter

from .perceptor import Perceptor
from .utils import validate_not_none, validate_type


class PerceptorNode:
    def __init__(self, perceptor_name, perceptor, multi=False, accelerator_idx=None):
        validate_not_none(perceptor, "perceptor is required")
        validate_type(perceptor, Perceptor, "perceptor must be an instance of Perceptor")

        validate_not_none(perceptor_name, "perceptor_name is required")
        validate_type(perceptor_name, str, "perceptor_name must be a string")

        self.accelerator_idx = accelerator_idx
        self.multi = multi

        self.__name = perceptor_name
        self.__perceptor = perceptor
        self.__child_perceptors = []

        # self.__perceptor.load(accelerator_idx)


    def add_child_perceptor(self, perceptor_node):
        validate_not_none(perceptor_node, "perceptor_node is required")
        validate_type(perceptor_node, str, "perceptor_node must be a string")

        self.__child_perceptors.append(perceptor_node)


    def get_child_perceptors(self):
        return self.__child_perceptors


    def run(self, input_data):
        result = self.__perceptor.run(input_data)
        print("finished running %s" % self.__str__())

        return result


    def __str__(self):
        return "PerceptorNode { name: %s }" % self.__name

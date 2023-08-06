import threading


class ProcessingEngine():
    def __init__(self, number_of_edge_tpus):
        self.__edge_tpu_locks = [threading.Lock() for _ in range(number_of_edge_tpus)]


    def run(self, perceptor_node, input_data):
        self.__edge_tpu_locks[perceptor_node.accelerator_idx].acquire()
        print("running %s" % perceptor_node)

        try:
            if perceptor_node.multi:
               return [perceptor_node.run(data) for data in input_data]
            else:
                return perceptor_node.run(input_data)
        finally:
            self.__edge_tpu_locks[perceptor_node.accelerator_idx].release()

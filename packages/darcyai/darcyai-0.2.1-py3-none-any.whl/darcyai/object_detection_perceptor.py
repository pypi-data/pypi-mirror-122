import time
from pycoral.utils import edgetpu
from random import random
from .perceptor import Perceptor


class ObjectDetectionPerceptor(Perceptor):
    def __init__(self, threshold, **kwargs):
        super().__init__(**kwargs)

        self.__threshold = threshold
        self.__interpreter = None


    def run(self, input_data):
        processed_input_data = self.input_callback(input_data)
        time.sleep(int(random() * 4) + 1)

        result = "Hello!!!"
        if self.output_callback is not None:
            result = self.output_callback(result)

        return result        


    def load(self, accelerator_idx):
        if accelerator_idx is None:
            self.__interpreter = edgetpu.make_interpreter(perceptor.model_path)
        else:
            self.__interpreter = edgetpu.make_interpreter(perceptor.model_path, device=':%s' % accelerator_idx)

        self.__interpreter.allocate_tensors()

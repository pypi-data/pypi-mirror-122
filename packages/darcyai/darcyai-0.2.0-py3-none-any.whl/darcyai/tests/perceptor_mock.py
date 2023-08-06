import time
from random import random
from ..perceptor import Perceptor


class PerceptorMock(Perceptor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def run(self, input_data):
        processed_input_data = self.input_callback(input_data)
        time.sleep(int(random() * 4) + 1)

        result = "Hello!!!"
        if self.output_callback is not None:
            result = self.output_callback(result)

        return result        

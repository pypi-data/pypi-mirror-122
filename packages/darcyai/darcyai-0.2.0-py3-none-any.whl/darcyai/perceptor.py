from .utils import validate_not_none


class Perceptor():
    def __init__(self, model_path, input_callback, output_callback=None):
        validate_not_none(model_path, "model_path is required")
        validate_not_none(input_callback, "input_callback is required")

        self.model_path = model_path
        self.input_callback = input_callback
        self.output_callback = output_callback


    def run(self, input_data):
        raise NotImplementedError("Perceptor.run() is not implemented")


    def load(self, accelerator_idx):
        raise NotImplementedError("Perceptor.load() is not implemented")
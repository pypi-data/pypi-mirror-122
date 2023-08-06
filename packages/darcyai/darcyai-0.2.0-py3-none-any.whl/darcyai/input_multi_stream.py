from collections.abc import Iterable
import threading
from .input_stream import InputStream
from .utils import validate_not_none, validate_type


class InputMultiStream:
    def __init__(self, aggregator, callback):
        validate_not_none(aggregator, "aggregator is required")
        validate_not_none(callback, "callback is required")

        self.__callback = callback
        self.__aggregator = aggregator

        self.__input_streams = {}
        self.__input_stream_threads = {}
        self.__stopped = True

    
    def __start_stream(self, stream_name):
        input_stream = self.__input_streams[stream_name]
        stream = input_stream.stream()
        validate_type(stream, Iterable, "stream %s is not of type Iterable" % stream_name)

        for data in stream:
            self.__callback(stream_name, data)


    def remove_stream(self, name):
        if not name in self.__input_streams:
            return

        self.__input_streams[name].stop()
        if name in self.__input_stream_threads:
            self.__input_stream_threads.pop(name)

        self.__input_streams.pop(name)


    def get_stream(self, name):
        if not name in self.__input_streams:
            return None

        return self.__input_streams[name]


    def add_stream(self, name, stream):
        validate_type(stream, (InputStream, InputMultiStream), "stream is not of type InputStream")
        if name in self.__input_streams:
            raise Exception("stream with name %s already exists" % name)

        self.__input_streams[name] = stream

        if not self.__stopped:
            self.__input_stream_threads[name] = threading.Thread(target=self.__start_stream, args=[name])
            self.__input_stream_threads[name].start()


    def stream(self):
        if len(self.__input_streams) == 0:
            raise Exception("at least 1 stream is required")

        self.__stopped = False

        for stream_name in self.__input_streams.keys():
            self.__input_stream_threads[stream_name] = threading.Thread(target=self.__start_stream, args=[stream_name])
            self.__input_stream_threads[stream_name].start()

        while not self.__stopped:
            data = self.__aggregator()

            yield(data)


    def stop(self):
        for stream in self.__input_streams.values():
            stream.stop()

        self.__stopped = True

from collections.abc import Iterable
import threading
from .output_stream import OutputStream
from .utils import validate_not_none, validate_type


class OutputMultiStream:
    def __init__(self, aggregator, callback):
        validate_not_none(aggregator, "aggregator is required")
        validate_not_none(callback, "callback is required")

        self.__callback = callback
        self.__aggregator = aggregator

        self.__output_streams = {}
        self.__output_stream_threads = {}
        self.__stopped = True

    
    def __start_stream(self, stream_name):
        output_stream = self.__output_streams[stream_name]
        stream = output_stream.stream()
        validate_type(stream, Iterable, "stream %s is not of type Iterable" % stream_name)

        for data in stream:
            self.__callback(stream_name, data)


    def remove_stream(self, name):
        if not name in self.__output_streams:
            return

        self.__output_streams[name].stop()
        if name in self.__output_stream_threads:
            self.__output_stream_threads.pop(name)

        self.__output_streams.pop(name)


    def get_stream(self, name):
        if not name in self.__output_streams:
            return None

        return self.__output_streams[name]


    def add_stream(self, name, stream):
        validate_type(stream, (OutputStream, OutputMultiStream), "stream is not of type OutputStream")

        if name in self.__output_streams:
            raise Exception("stream with name %s already exists" % name)

        self.__output_streams[name] = stream

        if not self.__stopped:
            self.__output_stream_threads[name] = threading.Thread(target=self.__start_stream, args=[name])
            self.__output_stream_threads[name].start()


    def stream(self):
        if len(self.__output_streams) == 0:
            raise Exception("at least 1 stream is required")

        self.__stopped = False

        for stream_name in self.__output_streams.keys():
            self.__output_stream_threads[stream_name] = threading.Thread(target=self.__start_stream, args=[stream_name])
            self.__output_stream_threads[stream_name].start()

        while not self.__stopped:
            data = self.__aggregator()

            yield(data)


    def stop(self):
        for stream in self.__output_streams.values():
            stream.stop()

        self.__stopped = True

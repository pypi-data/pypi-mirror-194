# Copyright (c) 2012-2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('StreamEmitter','Signal')

from .__config__ import origin
origin = __import__(origin, globals(), locals(), ["QtCore"], 0)


class StreamEmitter(origin.QtCore.QObject):

    message = origin.QtCore.Signal(object)

    def write(self, data):
        self.message.emit(data)

    def flush(self):
        pass


class Signal:

    def __init__(self):
        self._listeners = []

    def connect(self, listener):
        self._listeners.append(listener)

    def disconnect(self, listener):
        self._listeners.remove(listener)

    def emit(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)

    def __iadd__(self, listener):
        self.connect(listener)
        return self

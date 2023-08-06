import time
from varname import nameof


def validate_not_none(property, message):
    if property is None:
        raise Exception(message)


def validate_type(property, clazz, message):
    if not isinstance(property, clazz):
        raise Exception(message)


def timestamp():
    return int(time.time() * 1000)
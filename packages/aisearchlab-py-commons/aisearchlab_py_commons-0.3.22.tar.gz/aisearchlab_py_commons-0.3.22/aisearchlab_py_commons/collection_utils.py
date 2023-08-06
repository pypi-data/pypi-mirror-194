"""
Collection utils
"""
from itertools import chain, islice
from typing import Dict, Union, Any


def fget(obj: Union[None, Dict],
         field: str, silent=False,
         default: Any = None) -> Any:
    """
    Gets a field from object, fails with object details in error
    if field is missing
    """
    if obj is None and not silent:
        raise ValueError('object passed is None')
    elif obj is None:
        return default
    value = obj.get(field)
    if value is None and not silent:
        raise ValueError(
            'No {} in object {}'.format(field, obj))
    elif value is None:
        return default
    return value


def chunks(iterable, size=10):
    """
    Splits list in chunks of size n
    """
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))

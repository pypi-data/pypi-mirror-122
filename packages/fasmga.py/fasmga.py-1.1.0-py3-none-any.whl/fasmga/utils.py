import typing
from operator import attrgetter

T = typing.TypeVar('T')

class DictWithoutNones(dict):
    """A `dict` subclass that removes keys with `None` as value."""

    def __init__(self, *args, **_kwargs):
        kwargs = {}
        for k, v in _kwargs.items():
            if v != None:
                kwargs[k] = v
        return super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if value == None:
            return
        return super().__setitem__(key, value)


class TotallyARunningLoop:
    """This is totally a running loop."""

    def cancel(self):
        """This totally stops the totally running loop."""
        return
    
def get(iterable: typing.Iterable[T], **attrs: typing.Any) -> typing.Optional[T]:
    """A helper that returns the first element in the iterable that meets
    all the traits passed in ``attrs``. Stolen from discord.py"""
    _all = all
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace('__', '.'))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [(attrget(attr.replace('__', '.')), value) for attr, value in attrs.items()]

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            return elem
    return None

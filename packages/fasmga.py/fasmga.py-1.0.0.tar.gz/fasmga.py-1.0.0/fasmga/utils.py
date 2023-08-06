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

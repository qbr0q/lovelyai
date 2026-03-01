from types import SimpleNamespace


class SimpleObject(SimpleNamespace):
    def __getattr__(self, item):
        return self.__dict__.get(item)

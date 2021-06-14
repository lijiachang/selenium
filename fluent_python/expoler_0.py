from collections import abc


class FrozenJSON:
    def __init__(self, mapping):
        self._data = dict(mapping)  # 1.确保传入的是字典  2.安全起见，创建一个副本

    def __getattr__(self, item):
        if hasattr(self._data, item):
            return self._data.items
        else:
            return FrozenJSON.build(self._data[item])  # 注意找不到key的情况，会抛出异常，也是符合预期

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return list(obj)
        else:
            return obj

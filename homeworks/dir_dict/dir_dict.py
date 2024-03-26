import os
from collections.abc import MutableMapping


class MyDict(MutableMapping):
    def __init__(self, path):
        if os.path.exists(path):
            self._path = path
        else:
            raise ValueError(path)

    def __setitem__(self, key, value):
        with open(os.path.join(self._path, str(key)), "w") as f:
            f.write(str(value))

    def __getitem__(self, item):
        with open(os.path.join(self._path, str(item)), "r") as f:
            return f.read()

    def __delitem__(self, key):
        file_path = os.path.join(self._path, str(key))
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise KeyError(key)

    def __iter__(self):
        for file_name in os.listdir(self._path):
            yield file_name

    def __len__(self):
        return len(os.listdir(self._path))

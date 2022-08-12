from collections import ChainMap
from typing import Any, Dict
from contextlib import contextmanager


class DefaultListChainMap(ChainMap):
    """
    Превый элемент хранит значения всех остальных детей
    """

    def __setitem__(self, key, value):
        self.maps[0][key] = value
        if len(self.maps) > 1:
            mapping: Dict[str, Any] = self.maps[-1]
            if key not in mapping:
                mapping[key] = []
            mapping[key].append(value)

    @contextmanager
    def child(self):
        yield self.new_child(), False

    @contextmanager
    def parent(self):
        yield self, True

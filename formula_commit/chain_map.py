from collections import ChainMap
from typing import Any, Dict, List
from contextlib import contextmanager


class DefaultListChainMap(ChainMap):
    """
    Превый элемент хранит значения всех остальных детей
    """

    def __setitem__(self, key, value):
        self.maps[0][key] = value
        if len(self.maps) > 1:
            mapping: Dict[str, List[Any]] = self.maps[-1]
            mapping[key].append(value)

    @contextmanager
    def child(self):
        yield self.new_child()

    @contextmanager
    def parent(self):
        yield self

    def is_parent(self) -> bool:
        return len(self.maps) == 1

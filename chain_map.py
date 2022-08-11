from collections import ChainMap
from typing import Any, Dict


class DefaultListChainMap(ChainMap):
    def __setitem__(self, key, value):
        self.maps[0][key] = value
        if len(self.maps) > 1:
            mapping: Dict[str, Any] = self.maps[-1]
            if key not in mapping:
                mapping[key] = []
            mapping[key].append(value)

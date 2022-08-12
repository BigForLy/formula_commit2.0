from .functions import AvgFunc, IfFunc
from typing import Dict, Callable
from .functions import BaseFunc

FUNC_CALLABLE: Dict[str, BaseFunc] = {"avg": AvgFunc(), "if": IfFunc()}

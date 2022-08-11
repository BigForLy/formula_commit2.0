from .functions import AvgFunc
from typing import Dict, Callable

FUNC_CALLABLE: Dict[str, Callable] = {"avg": AvgFunc()}

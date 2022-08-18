from .functions import AvgFunc, IfFunc, OnlyFunc, CountFunc, SumFunc
from typing import Dict
from .functions import BaseFunc

FUNC_CALLABLE: Dict[str, BaseFunc] = {
    "avg": AvgFunc(),
    "if_": IfFunc(),
    "only": OnlyFunc(),
    "count": CountFunc(),
    "sum": SumFunc(),
}

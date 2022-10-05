from .functions import (
    AvgFunc,
    IfFunc,
    OnlyFunc,
    CountFunc,
    SumFunc,
    ReplaceFunc,
    SqrtFunc,
    MaxFunc,
    MinFunc,
    IfNullFunc,
)
from typing import Dict
from .functions import BaseFunc

FUNC_CALLABLE: Dict[str, BaseFunc] = {
    "avg": AvgFunc(),
    "if_": IfFunc(),
    "only": OnlyFunc(),
    "count": CountFunc(),
    "sum": SumFunc(),
    "replace": ReplaceFunc(),
    "sqrt": SqrtFunc(),
    "max": MaxFunc(),
    "min": MinFunc(),
    "ifnull": IfNullFunc(),
}

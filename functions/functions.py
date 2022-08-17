from __future__ import with_statement
from typing import Any, List, Tuple
from statistics import mean


class BaseFunc:
    def __init__(self) -> None:
        self.is_global = True  # взаимодействует со всеми определениями


class AvgFunc(BaseFunc):
    def __call__(self, args: List[Any]) -> Any:
        if len(args):
            return mean(args)
        return 0


class IfFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    def __call__(self, *args: Tuple[Any]) -> Any:
        assert len(args) == 3, f"Некоректная формула: {args=}"
        condition = args[0]
        return args[1] if condition else args[2]


class OnlyFunc(BaseFunc):
    def __call__(self, *args: Tuple[Any]) -> Any:
        assert len(args) == 2 or len(args) == 3, f"Некоректная формула: {args=}"
        if not args[0]:
            return 0
        condition = len(set(args[0])) == 1
        success_result = args[0][0] if len(args) == 2 else args[1]
        failed_result = args[1] if len(args) == 2 else args[2]
        return success_result if condition else failed_result

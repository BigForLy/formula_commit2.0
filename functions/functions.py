from __future__ import with_statement
from typing import Any, List
from statistics import mean


class BaseFunc:
    def __init__(self) -> None:
        self.is_global = True  # взаимодействует со всеми определениями


class AvgFunc(BaseFunc):
    def __call__(self, args: List[Any]) -> Any:
        if len(args):
            return mean(args)


class IfFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    def __call__(self, *args: List[Any]) -> Any:
        assert len(args) == 3
        condition: bool = args[0]
        try:
            return args[1] if condition else args[2]
        except:
            raise ValueError("Синтаксическая ошибка")

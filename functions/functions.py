from __future__ import with_statement
from typing import Any, List
from statistics import mean


class BaseFunc:
    def __init__(self) -> None:
        self.is_global = True  # взаимодействует со всеми определениями


class AvgFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, args: List[Any]) -> Any:
        if len(args):
            return mean(args)
    
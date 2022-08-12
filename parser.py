from collections import deque
from decimal import Decimal
from typing import Any, Deque, Generator, Set
from functions import FUNC_CALLABLE


class ParserManager:
    def __init__(self):
        self.operators = {
            "+",
            "-",
            "*",
            "/",
            "(",
            " ",
            ",",
            "<",
            ">",
            "=",
            ")",
            "!",
        }  # garbage

    def _parse(self, formula) -> Generator[str, None, None]:
        param = ""
        for s in formula:
            if s in self.operators:
                if param:
                    yield param
                yield s
                param = ""
            else:
                param += s
        if param:
            yield param

    def is_global_dependency(self, formula) -> bool:
        return any([token.lower() in FUNC_CALLABLE for token in self._parse(formula)])

    def elements_with_text(self, text: str, search_element: str) -> Set[str]:
        return set(token for token in self._parse(text) if search_element in token)

    def replace(
        self, source_text: str, replacement_text: str, value: Any, all: bool
    ) -> Generator[str, None, None]:
        def _inner(param: str):
            if param == replacement_text:
                if all or not len(dq):
                    yield repr(value) if isinstance(value, (Decimal, list)) else value
                    return
            yield param

        dq: Deque[str] = deque()
        param = ""
        for s in source_text:
            if s in self.operators:
                if s == "(" and (
                    len(dq) > 0
                    or param.lower() in FUNC_CALLABLE
                    and FUNC_CALLABLE[param.lower()].is_global
                ):
                    dq.append(s)

                if param:
                    yield from _inner(param)
                if s == ")" and len(dq) > 0:
                    dq.pop()
                yield s
                param = ""
            else:
                param += s
        if param:
            yield from _inner(param)

from typing import Any, Deque, Generator, Set
from collections import deque
from formula_commit.consts import null
from formula_commit.types_ import Null
from formula_commit.decimal_ import MDecimal
from formula_commit.functions import FUNC_CALLABLE


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

    def elements_with_text(self, text: str, search_element: str) -> Set[str]:
        return set(token for token in self._parse(text) if search_element in token)

    def replace(
        self, source_text: str, replacement_text: str, value: Any, all_: bool
    ) -> Generator[str, None, None]:
        def _inner(param: str):
            if param.lower() == replacement_text.lower():
                if all_ and not dq and isinstance(value, list) and not value:
                    yield repr(null)
                    return
                if all_ or not dq:
                    yield repr(value) if isinstance(
                        value, (MDecimal, list, Null)
                    ) else value
                    return
            yield param

        dq: Deque[str] = deque()
        param = ""
        for s in source_text:
            if s in self.operators:
                if s == "(" and (
                    dq or param in FUNC_CALLABLE and FUNC_CALLABLE[param].is_global
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

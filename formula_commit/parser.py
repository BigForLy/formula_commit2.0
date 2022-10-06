from typing import Any, Deque, Generator, Iterable, Set
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
        self, source_text: Iterable, replacement_text: str, value: Any, all_: bool
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

    def safe_lower(self, source_text: str):
        def _inner(param: str):
            lower_param = param.lower()
            if (
                (lower_param in lower_python_func_name)
                or (lower_param in lower_python_constants)
                or (lower_param in mysql_syntax)
                or (lower_param in FUNC_CALLABLE)
            ):
                yield lower_param
            else:
                yield param

        mysql_syntax = {"end", "then", "when", "else", "and", "is", "not"}
        lower_python_func_name = {"sqrt"}
        lower_python_constants = {"null"}
        param = ""
        for s in source_text:
            if s in self.operators:
                yield from _inner(param)

                yield s
                param = ""
            else:
                param += s
        if param:
            yield from _inner(param)

    def converter(
        self,
        source_text: str,
        replacement_text: str,
        value: str,
        end_of_element: str,
        end_text: str,
    ):
        def _inner(text: str):
            is_replaced = False
            param = ""
            for s in text:
                if s in self.operators:
                    if param:
                        yield param

                    if s == end_of_element and n_bracket <= 0 and not is_replaced:
                        yield end_text
                        is_replaced = True
                    else:
                        yield s

                    param = ""
                else:
                    param += s
            if param:
                yield param

        if replacement_text in source_text:
            n_bracket = 0
            result = ""
            for element in source_text.split(replacement_text)[::-1]:
                if (local_result := "".join(_inner(element))) and element != "(":
                    result += value + local_result
                    continue
                # если не седлали замену элемента, то надо добавить последний элемент вконце
                # только в том случае если текст не пустой
                if not element or element[-1] != "(":  # если element
                    result += "')"
            return result
        return source_text

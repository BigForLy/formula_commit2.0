from typing import Iterable, Set
from functions import FUNC_CALLABLE


class ParserManager:
    def __init__(self):
        self.operators = {"+", "-", "*", "/", "(", " ", ",", "<", ">", "=", ")"}  # garbage

    def _parse(self, formula):
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

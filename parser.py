from functions import FUNC_CALLABLE


class ParserManager:
    def __init__(self):
        self.__OPERATORS = {"+", "-", "*", "/"}

    def _parse(self, formula):
        param = ""
        for s in formula:
            if s in self.__OPERATORS or s in "( ,<>=)":  # garbage
                if param:
                    yield param
                yield s
                param = ""
            else:
                param += s
        if param:
            yield param

    def is_global_dependency(self, formula):
        return any([token.lower() in FUNC_CALLABLE for token in self._parse(formula)])

    def get_dependency(self, formula):
        return set(token for token in self._parse(formula) if "@" in token)

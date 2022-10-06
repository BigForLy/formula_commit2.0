from formula_commit.parser import ParserManager
from formula_commit.functions import FUNC_CALLABLE


parser = ParserManager()


def if_converter(formula: str) -> str:
    """
    заменяет if на функцию if_
    """
    return "".join(parser.replace(formula, "if", "if_", True))


def function_converter(formula: str) -> str:
    """
    подготовка формулы
    """
    replace_dict = {"sqrt": ""}

    tmp_formula = formula
    for name, _ in FUNC_CALLABLE.items() | replace_dict.items():
        tmp_formula = tmp_formula.replace(name, "_" * len(name))
    tmp_formula = tmp_formula.lower()
    for name, _ in FUNC_CALLABLE.items() | replace_dict.items():
        if name in tmp_formula:
            formula = (
                formula[: tmp_formula.index(name)]
                + name
                + formula[tmp_formula.index(name) + len(name) :]
            )
    return formula

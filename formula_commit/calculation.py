from formula_commit.decimal_ import MDecimal
from formula_commit.consts import null
from formula_commit.functions import FUNC_CALLABLE


def calculation(formula: str):
    return eval(
        formula,
        {
            "__builtins__": {"round": round},
            "MDecimal": MDecimal,
            "null": null,
            **FUNC_CALLABLE,
            # eval really is dangerous
            "os": ValueError,
            "__import__": ValueError,
            "__class__": ValueError,
        },
    )

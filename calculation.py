from decimal_ import MDecimal
from consts import null
from functions import FUNC_CALLABLE


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

from formula_commit.decimal_ import MDecimal
from formula_commit.consts import null


def calculation(formula: str, **kwargs):
    return eval(
        formula,
        {
            "__builtins__": {"round": round},
            "MDecimal": MDecimal,
            "null": null,
            # eval really is dangerous
            "os": ValueError,
            "__import__": ValueError,
            "__class__": ValueError,
            # custom local scope
            **kwargs,
        },
    )

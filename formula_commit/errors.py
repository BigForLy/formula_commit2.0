from typing import List
from formula_commit.fields import BaseField


class ObserversNotEmpty(BaseException):
    msg = "Расчет подошел к концу, но наблюдатели не пусты"

    def __init__(self, observers: List[BaseField], /) -> None:
        obs = []
        for current_field in observers:
            obs.append(
                f"(symbol: {current_field.symbol}, definition_number:"
                f" {current_field.definition_number}, "
                f"formula: {current_field.formula})"
            )
        super().__init__(self.msg + " [" + ",".join(obs) + "]")

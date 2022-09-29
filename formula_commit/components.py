from abc import ABC, abstractmethod
from decimal import localcontext
from typing import TYPE_CHECKING
from formula_commit.decimal_ import MDecimal
from formula_commit.consts import null
from formula_commit.types_ import Null


if TYPE_CHECKING:
    from fields import BaseField


class IComponent(ABC):
    @abstractmethod
    def accept(self, visitor: "BaseField") -> Null | bool:
        pass


class ConcreteComponentRoundTo(IComponent):
    """
    округление
    """

    def accept(self, visitor: "BaseField") -> Null | bool:
        if visitor._value is null:  # TODO
            return null
        assert isinstance(visitor._value, MDecimal)
        is_need_rounding = visitor._value.as_tuple().exponent < visitor.round_to
        round_to_below_zero = visitor.round_to < 0
        match is_need_rounding, round_to_below_zero:
            case True, True:
                twoplaces = MDecimal(10) ** visitor.round_to
                visitor._value = visitor._value.quantize(twoplaces)
            case _, False:
                int_len = len(str(int(visitor._value)))  # TODO
                if int_len > visitor.round_to:
                    with localcontext() as ctx:
                        ctx.prec = int_len - visitor.round_to
                        visitor._value = +visitor._value  # type: ignore
        return True

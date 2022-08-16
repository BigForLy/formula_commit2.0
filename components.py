from abc import ABC, abstractmethod
from decimal import Decimal, localcontext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fields import BaseField


class Component(ABC):
    @abstractmethod
    def accept(self, visitor: "BaseField") -> None:
        pass


class ConcreteComponentRoundTo(Component):
    """
    округление
    """

    def accept(self, visitor: "BaseField") -> None:
        is_need_rounding = visitor.value.as_tuple().exponent < visitor.round_to
        round_to_below_zero = visitor.round_to < 0
        match is_need_rounding, round_to_below_zero:
            case True, True:
                twoplaces = Decimal(10) ** visitor.round_to
                visitor.value = visitor.value.quantize(twoplaces)
            case _, False:
                int_len = len(str(int(visitor.value)))
                if int_len > visitor.round_to:
                    with localcontext() as ctx:
                        ctx.prec = int_len - visitor.round_to
                        visitor.value = +visitor.value

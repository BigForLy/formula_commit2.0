from abc import ABC, abstractmethod
from decimal import localcontext
from decimal_ import MDecimal
from typing import TYPE_CHECKING
from consts import null
from types_ import Null

if TYPE_CHECKING:
    from fields import BaseField


class IComponent(ABC):
    @abstractmethod
    def accept(self, visitor: "BaseField") -> None | Null:
        pass


class ConcreteComponentRoundTo(IComponent):
    """
    округление
    """

    def accept(self, visitor: "BaseField") -> None | Null:  # type: ignore[return]
        if visitor.value is null:  # TODO
            return null
        assert isinstance(visitor.value, MDecimal)
        is_need_rounding = visitor.value.as_tuple().exponent < visitor.round_to
        round_to_below_zero = visitor.round_to < 0
        match is_need_rounding, round_to_below_zero:
            case True, True:
                twoplaces = MDecimal(10) ** visitor.round_to
                visitor.value = visitor.value.quantize(twoplaces)
            case _, False:
                int_len = len(str(int(visitor.value)))  # TODO
                if int_len > visitor.round_to:
                    with localcontext() as ctx:
                        ctx.prec = int_len - visitor.round_to
                        visitor.value = +visitor.value  # type: ignore

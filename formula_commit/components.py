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
        if visitor.value is null:
            return null
        assert isinstance(visitor.value, MDecimal)
        is_need_rounding = visitor.value.as_tuple().exponent < visitor.round_to
        round_to_below_zero = visitor.round_to < 0
        match is_need_rounding, round_to_below_zero:
            case True, True:
                twoplaces = MDecimal(10) ** visitor.round_to
                visitor.value = visitor.value.quantize(twoplaces)
            case _, False:
                # TODO: вероятно есть способ лучше для преобразования
                int_len = len(str(int(visitor.value)))
                if int_len > visitor.round_to:
                    with localcontext() as ctx:
                        ctx.prec = int_len - visitor.round_to
                        visitor.value = +visitor.value  # type: ignore
        return True


class ConcreteComponentRoundWithZero(IComponent):
    """
    дополнение нулями после запятой
    """

    def accept(self, visitor: "BaseField") -> str:
        if isinstance(visitor.value, MDecimal):
            visitor.value = f"{visitor.value:.{abs(visitor.round_to)}f}"

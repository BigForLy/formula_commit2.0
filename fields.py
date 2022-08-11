from abc import ABC, abstractmethod
from typing import Any, Set
import uuid
from typing import TYPE_CHECKING

from decimal import Decimal

if TYPE_CHECKING:
    from calculation import Group


class BaseField(ABC):
    def __init__(
        self,
        *,
        definition_number: int = 0,
        symbol: str,
        formula: str,
        value: int | float | str,
        primary_key: Any,
    ) -> None:
        self.value = value
        self.symbol = symbol
        self.formula = formula
        self._value_only = False  # значение является константой
        self.definition_number = definition_number
        self.dependence: Set[str] = set()
        self.primary_key = primary_key

    @abstractmethod
    def calc(self):
        """
        result processing method
        """
        raise NotImplementedError

    def create_symbol(self):
        self.symbol = str(f"@{uuid.uuid4()}")

    def update(self, subject: "Group") -> None:
        self.dependence = subject.parser.get_dependency(self.formula)
        for token in self.dependence:
            if token in subject.cm:
                element = subject.cm[token]
                self.formula = self.formula.replace(token, repr(element))
        self.dependence = subject.parser.get_dependency(self.formula)
        if not self.dependence:
            self.formula_calculation()
            subject.calculation_current_field(self)

    def formula_calculation(self):
        try:
            from decimal import Decimal
            self.value = eval(self.formula)
        except:
            raise


class NumericField(BaseField):
    def __init__(
        self,
        *,
        definition_number: int = 0,
        symbol: str,
        formula: str,
        value: int | float | str,
        primary_key: Any,
    ) -> None:
        super().__init__(
            definition_number=definition_number,
            symbol=symbol,
            formula=formula,
            value=value,
            primary_key=primary_key,
        )
        if value:  # может поменять на float('inf') / float('nan')
            self.value: Decimal = Decimal(value)

    def calc(self):
        pass
        # self.value = str(self.value)  # TODO: необходимо округлить значение


class StringField(BaseField):
    def calc(self):
        pass


class BoolField(BaseField):
    def calc(self):
        pass

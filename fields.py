from abc import ABC, abstractmethod
from typing import Any, Set, TYPE_CHECKING
import uuid
from decimal import Decimal
from consts import FIRST_SYMBOL_BY_ELEMENT
from functions import FUNC_CALLABLE
from parser import ParserManager

if TYPE_CHECKING:
    from calculation import Group

parser = ParserManager()


class BaseField(ABC):
    """
    Базовый класс для поля
    """

    def __init__(
        self,
        *,
        definition_number: int = 0,
        symbol: str,
        formula: str,
        value: int | float | str,
        primary_key: Any,
        round_to: int = 0,
        formula_check: str = "",
    ) -> None:
        self.value: int | float | str | Decimal = self.convert_value(value)
        self.symbol = symbol
        self.formula = formula
        self._value_only = False  # значение является константой
        self.definition_number = definition_number
        self.dependence: Set[str] = set()
        self.primary_key = primary_key

    def convert_value(self, value):
        return value

    @abstractmethod
    def calc(self):
        """
        result processing method
        """
        raise NotImplementedError

    def create_symbol(self):
        self.symbol = str(f"{FIRST_SYMBOL_BY_ELEMENT}{uuid.uuid4()}")

    def update(self, subject: "Group") -> None:
        self.dependence = parser.elements_with_text(
            self.formula, FIRST_SYMBOL_BY_ELEMENT
        )
        for token in self.dependence:
            if token in subject.cm:
                element = subject.cm[token]
                self.formula = "".join(
                    parser.replace(self.formula, token, element, subject.cm.is_parent())
                )
        self.dependence = parser.elements_with_text(
            self.formula, FIRST_SYMBOL_BY_ELEMENT
        )
        if not self.dependence:
            self.formula_calculation()
            subject.calculation_current_field(self)

    def formula_calculation(self):
        try:
            self.value = eval(self.formula, {"Decimal": Decimal, **FUNC_CALLABLE})
        except:
            raise

    def update_formula(self):
        self.formula = "".join(parser.replace(self.formula, "if", "if_", True))
        self.formula = (
            self.formula.replace("=", "==")
            .replace("<==", "<=")
            .replace(">==", ">=")
            .replace("<>", "!=")
        )


class NumericField(BaseField):
    """
    Числовое поле
    """

    def convert_value(self, value):
        return (
            Decimal(value)
            if value
            else value  # может поменять на float('inf') / float('nan')
        )

    def calc(self):
        pass
        # self.value = str(self.value)  # TODO: необходимо округлить значение


class StringField(BaseField):
    """
    Строковое поле
    """

    def calc(self):
        pass


class BoolField(BaseField):
    """
    Логическое поле
    """

    def calc(self):
        pass

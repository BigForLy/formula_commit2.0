from abc import ABC, abstractmethod
from typing import Any, List, Set, TYPE_CHECKING, Type
from decimal_ import MDecimal
from consts import null
import uuid
from parser import ParserManager
from components import IComponent, ConcreteComponentRoundTo
from consts import FIRST_SYMBOL_BY_ELEMENT
from functions import FUNC_CALLABLE

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
        formula_check: str = "",  # TODO
        round_with_zeros=None,  # TODO
    ) -> None:
        self._calc_component: List[Type[IComponent]] = []

        self.value: str | MDecimal | int = self.convert_value(value)

        self._update_round_to(round_to)

        self.symbol = symbol
        self.formula = formula
        self._value_only = False  # значение является константой
        self.definition_number = definition_number
        self.dependence: Set[str] = set()
        self.primary_key = primary_key

    def convert_value(self, value) -> str | MDecimal | int:
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
            if token in subject.cm.maps[0]:
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
            self.value = eval(
                self.formula, {"MDecimal": MDecimal, "null": null, **FUNC_CALLABLE}
            )
        except NameError as exc:
            # Обрабатываем исключение для StringField
            self.value = self.formula
        except (SystemExit, Exception) as exc:
            raise ValueError(
                f"Ошибка в формуле: symbol={self.symbol}, definition_number={self.definition_number}, formula={self.formula}"
            ) from exc

    def convert_to_python_formula(self):
        self.formula = "".join(parser.replace(self.formula, "if", "if_", True))
        self.formula = "".join(parser.replace(self.formula, "avg", "avg", True))  # TODO
        self.formula = "".join(parser.replace(self.formula, "replace", "replace", True))
        self.formula = (
            self.formula.replace("=", "==")
            .replace("<==", "<=")
            .replace(">==", ">=")
            .replace("<>", "!=")
        )

    def _update_value_with_component(self):
        for component in self._calc_component:
            component().accept(self)

    def _update_round_to(self, round_to):
        self.round_to = round_to
        if round_to:
            self._calc_component.append(ConcreteComponentRoundTo)


class NumericField(BaseField):
    """
    Числовое поле
    """

    def convert_value(self, value) -> str | MDecimal | int:
        return (
            MDecimal(str(value))
            if value
            else value  # может поменять на float('inf') / float('nan')
        )

    def calc(self):
        self._update_value_with_component()


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

    def convert_value(self, value) -> str | MDecimal | int:
        return 1 if value in (True, 1, "True") else 0

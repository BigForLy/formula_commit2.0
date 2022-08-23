from abc import ABC, abstractmethod
from decimal import InvalidOperation
from typing import Any, List, Set, TYPE_CHECKING, Type
import uuid
from parser import ParserManager
from components import IComponent, ConcreteComponentRoundTo
from decimal_ import MDecimal
from consts import null
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
        required_field: bool = True,  # TODO
    ) -> None:
        self._calc_component: List[Type[IComponent]] = []
        self.required_field = required_field
        self.formula = formula
        self.symbol = symbol
        self._value_only = False  # значение является константой
        self.definition_number = definition_number
        self.primary_key = primary_key
        self.dependence: Set[str] = set()

        self._value: str | MDecimal | int = self.convert_value(value)

        self._update_round_to(round_to)

    def convert_value(self, value) -> str | MDecimal | int:
        return value

    def check_required_field(self):
        if self.required_field and self._value in ("", None) and not self.formula:
            raise ValueError(f"Не заполнено обязательное поле: (symbol: {self.symbol})")

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
            # вызывает последовательное обновление столбцов
            subject.calculation_current_field(self)

    def formula_calculation(self):
        try:
            value = eval(
                self.formula,
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
            if isinstance(value, (int, float)):  # TODO
                value = MDecimal(str(value))
            self._value = value
        except (SystemExit, Exception) as exc:
            raise ValueError(
                f"Ошибка в формуле: symbol={self.symbol}, definition_number={self.definition_number}, formula={self.formula}"
            ) from exc

    def convert_to_python_formula(self):
        self.formula = "".join(parser.replace(self.formula, "if", "if_", True))
        self.formula = "".join(parser.replace(self.formula, "avg", "avg", True))  # TODO
        self.formula = "".join(parser.replace(self.formula, "replace", "replace", True))
        self.formula = "".join(parser.replace(self.formula, "sqrt", "sqrt", True))
        self.formula = "".join(parser.replace(self.formula, "<>", "!=", True))
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

    def value(self):
        return self._value


class NumericField(BaseField):
    """
    Числовое поле
    """

    def convert_value(self, value) -> str | MDecimal | int:
        try:
            return (
                MDecimal(str(value))
                if value
                else value  # может поменять на float('inf') / float('nan')
            )
        except InvalidOperation as exc:
            raise ValueError(
                f"В числовое поле записана строка: symbol={self.symbol}"
            ) from exc
        except Exception as exc:
            raise Exception from exc

    def calc(self):
        if self._value:
            self._update_value_with_component()


class StringField(BaseField):
    """
    Строковое поле
    """

    def convert_value(self, value) -> str | MDecimal | int:
        try:
            value = MDecimal(value)
        except:
            value = repr(value)
        finally:
            return value

    def calc(self):
        if isinstance(self._value, MDecimal):
            self._update_value_with_component()
        if isinstance(self._value, str) and not self.value_is_repr():
            self._value = repr(self._value)

    def value(self):
        if self.value_is_repr():
            return self._value[1:-1]
        return self._value

    def value_is_repr(self):
        return (
            isinstance(self._value, str)
            and len(self._value) > 1
            and self._value[0] in ("'", '"')
            and self._value[-1] in ("'", '"')
        )


class BoolField(BaseField):
    """
    Логическое поле
    """

    def calc(self):
        pass

    def convert_value(self, value) -> str | MDecimal | int:
        return 1 if value in (True, 1, "True") else 0

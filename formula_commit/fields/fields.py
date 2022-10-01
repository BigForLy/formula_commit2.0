import uuid
from abc import ABC, abstractmethod
from decimal import InvalidOperation
from typing import Any, List, Set, TYPE_CHECKING, Type
from formula_commit.parser import ParserManager
from formula_commit.calculation import calculation
from formula_commit.components import IComponent, ConcreteComponentRoundTo
from formula_commit.decimal_ import MDecimal
from formula_commit.consts import FIRST_SYMBOL_BY_ELEMENT

if TYPE_CHECKING:
    from group import Group

parser = ParserManager()


class IField(ABC):
    @abstractmethod
    def convert_value(self, value) -> str | MDecimal | int | bool:
        """ """
        raise NotImplementedError

    @abstractmethod
    def calc(self):
        """
        result processing method
        """
        raise NotImplementedError

    @abstractmethod
    def value(self):
        raise NotImplementedError


class BaseField(IField, ABC):
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
        **kwargs,
    ) -> None:
        self._calc_component: List[Type[IComponent]] = []
        self.required_field = required_field
        self.formula = formula
        self.__symbol_update(symbol)
        self._value_only = False  # значение является константой
        self.definition_number = definition_number
        self.primary_key = primary_key
        self.dependence: Set[str] = set()

        self.value = value

        self._update_round_to(round_to)

    def __symbol_update(self, symbol):
        if self.__is_need_creating_symbol(symbol):
            symbol = self.__creating_symbol()
        if not self.__is_symbol_correct(symbol):
            symbol = self.__symbol_adjustment(symbol)

        self.symbol = symbol

    @staticmethod
    def __is_symbol_correct(symbol):
        if symbol and symbol[0] == FIRST_SYMBOL_BY_ELEMENT:
            return True
        return False

    @staticmethod
    def __symbol_adjustment(symbol):
        return FIRST_SYMBOL_BY_ELEMENT + symbol

    @staticmethod
    def __is_need_creating_symbol(symbol):
        if not symbol:
            return True
        return False

    @staticmethod
    def __creating_symbol():
        return str(uuid.uuid4())

    def check_required_field(self):
        if self.required_field and self._value in ("", None) and not self.formula:
            raise ValueError(
                f"Не заполнено обязательное поле: "
                f"(symbol: {self.symbol}, value: {self._value})"
            )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value: str | MDecimal | int = self.convert_value(value)

    @property
    def is_need_update(self) -> bool:
        return bool(self.formula and not self._value_only)

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
            # вызывает последовательное обновление полей
            subject.calculation_current_field(self)

    def formula_calculation(self):
        try:
            value = calculation(self.formula)
            if isinstance(value, (int, float)):  # TODO
                value = MDecimal(str(value))
            self._value = value
        except (SystemExit, Exception) as exc:
            raise ValueError(
                f"Ошибка в формуле: symbol={self.symbol}, "
                f"definition_number={self.definition_number}, "
                f"formula={self.formula}"
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

    def _update_value_with_components(self):
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
            self._update_value_with_components()


class StringField(BaseField):
    """
    Строковое поле
    """

    def convert_value(self, value) -> str | MDecimal | int:
        try:
            return MDecimal(value)
        except InvalidOperation:
            return repr(value)

    def calc(self):
        if isinstance(self._value, MDecimal):
            self._update_value_with_components()
        if isinstance(self._value, str) and not self.value_is_repr():
            self._value = repr(self._value)

    @property
    def value(self):
        if self.value_is_repr():
            return self._value[1:-1]
        return self._value

    @value.setter
    def value(self, value):
        self._value: str | MDecimal | int = self.convert_value(value)

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

    @property
    def value(self):
        return True if self._value else False

    def convert_value(self, value) -> str | MDecimal | int:
        if value in (True, 1, "True"):
            return 1
        elif value in (False, 0, "False"):
            return 0
        assert False, f"Некорректное значение для BoolField. value: {value}"

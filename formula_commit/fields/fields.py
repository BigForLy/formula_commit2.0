from types import NoneType
import uuid
from abc import ABC, abstractmethod
from decimal import InvalidOperation
from typing import Any, List, Set, TYPE_CHECKING, Type
from formula_commit.functions import FUNC_CALLABLE
from formula_commit.parser import ParserManager
from formula_commit.calculation import calculation
from formula_commit.components import (
    ComponentContrRoundWithZero,
    ComponentRoundWithZero,
    IComponent,
    ComponentRoundTo,
)
from formula_commit.decimal_ import MDecimal
from formula_commit.consts import FIRST_SYMBOL_BY_ELEMENT, null
from formula_commit.types_ import Null

if TYPE_CHECKING:
    from group import Group

parser = ParserManager()


class IField(ABC):
    @abstractmethod
    def _convert_value(self, value) -> str | MDecimal | int | bool:
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
        formula_check: str = "",  # TODO: не реализованно
        is_round_with_zeros: bool = False,
        is_required: bool = True,
        **kwargs,
    ) -> None:
        self._calc_component: List[Type[IComponent]] = []
        self.is_required = is_required
        self.__symbol_update(symbol)
        self.formula = formula
        # изначально считаем, что поле рассчитывается по формуле
        self._value_only = False
        self.definition_number = definition_number
        self.primary_key = primary_key
        self.dependence: Set[str] = set()
        self.value = value

        self.round_to = round_to

        self.__is_round_with_zeros = is_round_with_zeros

        self.__formula_check = formula_check

        self.__component_order()

    def __component_order(self):
        """
        Устанавливает компоненты и их порядок
        """
        if self.round_to:
            self._calc_component.append(ComponentRoundTo)
        if self.__is_round_with_zeros:
            self._calc_component.append(ComponentRoundWithZero)
        else:
            self._calc_component.append(ComponentContrRoundWithZero)

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
        if self.is_required and self._value in ("", None) and not self.formula:
            raise ValueError(
                f"Не заполнено обязательное поле: "
                f"(symbol: {self.symbol}, value: {self._value})"
            )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value: str | MDecimal | int = self._convert_value(value)

    @property
    def get_result_value(self):
        """
        метод для предоставления значения в результат расчета
        """
        return str(self._value)

    @property
    def is_need_update(self) -> bool:
        return bool(self.formula and not self._value_only)

    def update(self, subject: "Group") -> None:
        self.dependence = parser.elements_with_text(
            self.formula, FIRST_SYMBOL_BY_ELEMENT
        )
        for token in self.dependence:
            if token in subject.cm:  # сотреть __contains__
                token_value = subject.cm[token]  # смотреть __getitem__
                # заменяем зависимости, у которых есть значение
                self.formula = "".join(
                    parser.replace(
                        self.formula,
                        token,
                        token_value,
                        subject.cm.is_parent,
                    )
                )
        self.dependence = parser.elements_with_text(
            self.formula, FIRST_SYMBOL_BY_ELEMENT
        )

        # подписываемся на зависимости
        for item in self.dependence:
            subject.attach(self, item)

        # если нет зависимостей записываем значения
        if not self.dependence:
            # расчет поля
            self.formula_calculation()
            # вызывает расчет поля и последовательное обновление полей
            subject.calculation_current_field(self)

    def update_with_elements(self, subject: "Group"):
        for token in self.dependence:
            if token in subject.cm.elements:
                token_value = null
                self.formula = "".join(
                    parser.replace(
                        self.formula,
                        token,
                        token_value,
                        subject.cm.is_parent,
                    )
                )
        self.dependence = parser.elements_with_text(
            self.formula, FIRST_SYMBOL_BY_ELEMENT
        )

        # подписываемся на зависимости
        for item in self.dependence:
            subject.attach(self, item)

        # если нет зависимостей записываем значения
        if not self.dependence:
            # расчет поля
            self.formula_calculation()
            # вызывает расчет поля и последовательное обновление полей
            subject.calculation_current_field(self)

    def formula_calculation(self):
        try:
            value = calculation(self.formula, **FUNC_CALLABLE)
            if isinstance(value, (int, float)):
                value = MDecimal(str(value))
            self.value = value
        except (SystemExit, Exception) as exc:
            raise ValueError(
                f"Ошибка в формуле: symbol={self.symbol}, "
                f"definition_number={self.definition_number}, "
                f"formula={self.formula}"
            ) from exc

    def convert_to_python_formula(self):
        self.formula = "".join(parser.replace(self.formula, "if", "if_", True))
        self.formula = self.formula.replace("\r\n", " ")
        self.formula = "".join(parser.safe_lower(self.formula))
        # рассчитываем что перед case when всегда будет скобочка
        # не через парсер потому что меняем позицию скобки
        self.formula = "".join(
            parser.converter(self.formula, "case when", 'case_when("', ")", '")')
        )
        # убираем лишние символы
        self.formula = "".join(parser.replace(self.formula, "<>", "!=", True))
        self.formula = "".join(
            parser.replace(self.formula, self.symbol, self.value, True)
        )
        self.formula = (
            self.formula.replace("=", "==")
            .replace("<==", "<=")
            .replace(">==", ">=")
            .replace("<>", "!=")
        )

    def _update_value_with_components(self):
        for component in self._calc_component:
            component().accept(self)

    def __repr__(self) -> str:
        return (
            f"definition_number={self.definition_number}, symbol={self.symbol}, "
            f"formula={self.formula}, value={str(self.value)}, primary_key="
            f"{self.primary_key}, round_to={self.round_to},"
            f" formula_check={self.__formula_check}, round_with_zeros="
            f"{self.__is_round_with_zeros}, required_field={self.is_required}"
        )

    def _is_convert_to_int(self):
        return (
            isinstance(self.value, MDecimal) and self.value.as_integer_ratio()[1] == 1
        )


class NumericField(BaseField):
    """
    Числовое поле
    """

    def _convert_value(self, value) -> str | MDecimal | int:
        try:
            if isinstance(value, str):
                value = value.replace(",", ".")
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

    @property
    def value(self):
        # в случае, если поле не обязательное для расчета используем null
        if self._value == "":
            return null
        return self._value

    @value.setter
    def value(self, value):
        self._value: str | MDecimal | int = self._convert_value(value)

    @property
    def get_result_value(self):
        """
        метод для предоставления значения в результат расчета
        """
        if not self.is_required and self._value is null:
            return ""
        if self._is_convert_to_int():
            return str(int(self._value))
        return str(self._value)

    def calc(self):
        if self._value:
            self._update_value_with_components()

    def __repr__(self) -> str:
        return f"NumericField({super().__repr__()})"


class StringField(BaseField):
    """
    Строковое поле
    """

    def _convert_value(self, value) -> str | MDecimal | Null:
        try:
            return MDecimal(value)
        except InvalidOperation:
            return value
        except TypeError as exc:
            if value is null:
                return null
            raise ValueError(
                "Не удалось изменить значение строкового поля на значение: " + value
            ) from exc

    def calc(self):
        if isinstance(self._value, MDecimal):
            self._update_value_with_components()

    @property
    def get_result_value(self):
        """
        метод для предоставления значения в результат расчета
        """
        if not self.is_required and self._value is null:
            return ""
        if self._is_convert_to_int():
            return str(int(self._value))
        return str(self._value)  # кастит значение из MDecimal в str

    def __repr__(self) -> str:
        return f"StringField({super().__repr__()})"


class BoolField(BaseField):
    """
    Логическое поле
    """

    def calc(self):
        pass

    @property
    def get_result_value(self):
        """
        метод для предоставления значения в результат расчета
        """
        return "True" if self._value else "False"

    def _convert_value(self, value) -> str | MDecimal | int:
        if value in (True, 1, "True"):
            return 1
        elif value in (False, 0, "False"):
            return 0
        assert False, f"Некорректное значение для BoolField. value: {value}"

    def __repr__(self) -> str:
        return f"BoolField({super().__repr__()})"

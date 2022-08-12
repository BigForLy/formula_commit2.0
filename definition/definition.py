from collections import deque
from typing import Deque, TYPE_CHECKING
from parser import ParserManager

if TYPE_CHECKING:
    from fields import BaseField


class Definition:
    def __init__(self):
        self.__check_ignore = False
        self.__input_manual = False
        self.parser = ParserManager()
        # fields учавствующие в расчете
        self.local_deque: Deque["BaseField"] = deque()

    def add_field(self, current_field: "BaseField"):
        # все значения полей после активации флага становятся константами
        if self.__input_manual or self.__check_ignore:
            # Если установлен параметр ввод вручную или игнорировать, поля не должны менять свое значение
            current_field._value_only = True

        # Если у current_field не заполнен символ, создаем его
        if not current_field.symbol:
            current_field.create_symbol()

        if not self.__check_ignore:
            # Если у определения не активен параметр игнорировать, добавляем поле в расчет
            self.add_in_deque(current_field)

        if "check_ignore" in current_field.symbol and current_field.value:
            self.__check_ignore = True
            self.local_deque.clear()
        elif "input_manual" in current_field.symbol and current_field.value:
            self.__input_manual = True
            self.local_deque.clear()

    def add_in_deque(self, current_field: "BaseField"):
        if current_field.formula:
            # TODO: bad bad bad
            current_field.formula = "".join(
                self.parser.replace(current_field.formula, "if", "if_", True)
            )
            current_field.formula = (
                current_field.formula.replace("=", "==")
                .replace("<==", "<=")
                .replace(">==", ">=")
                .replace("<>", "!=")
            )
            self.local_deque.append(current_field)
        else:
            self.local_deque.appendleft(current_field)

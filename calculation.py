from collections import deque
from typing import Deque
from chain_map import DefaultListChainMap
from errors import ObserversNotEmpty
from fields import BaseField
from observer import Subject


class Calculation:
    def __init__(self) -> None:
        self.group_list: Deque[Group] = deque()

    def add_group(self, dq: Deque[BaseField], cm: DefaultListChainMap):
        self.group_list.append(Group(dq, cm))

    def start(self):
        while self.group_list:
            group = self.group_list.popleft()
            group.calc()
            # Проверяем что обсерверы пусты, иначе одна из формул оказалась глобальной
            if not group.is_observers_empty:
                # Если обсерверы были в последней группе, возвращаем ошибку
                if not self.group_list:
                    raise ObserversNotEmpty(group.pop_observers())
                self.last_group.dq.extend(group.pop_observers())

    @property
    def last_group(self):
        return self.group_list[-1]


class Group(Subject):  # Group == Definition
    def __init__(self, dq: Deque[BaseField], cm: DefaultListChainMap) -> None:
        self.dq = dq
        self.cm = cm
        super().__init__()

    def calc(self):
        while self.dq:
            current_field = self.dq.popleft()
            current_field.check_required_field()
            if current_field.formula and not current_field._value_only:
                current_field.update(self)
                if current_field.dependence:
                    self.attach(
                        current_field
                    )  # TODO: реализовать подписку на конкретные атрибуты
            else:
                self.calculation_current_field(current_field)

    def calculation_current_field(self, current_field: "BaseField"):
        current_field.calc()
        self.cm.update({current_field.symbol: current_field.value})
        self.detach(current_field)  # type: ignore
        self.notify()

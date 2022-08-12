from collections import deque, ChainMap
from typing import Deque, Tuple
from parser import ParserManager
from fields import BaseField
from observer import Subject


class Calculation:
    def __init__(self) -> None:
        self.group_list: Deque[Group] = deque()

    def add_group(self, dq: Deque[BaseField], cm: Tuple[ChainMap, bool]):  # TODO: rename element
        self.group_list.append(Group(dq, cm[0], cm[1]))

    def start(self):
        while self.group_list:
            group = self.group_list.popleft()
            group.calc()
            # Проверяем что обсерверы пусты, иначе одна из формул оказалась глобальной
            if not group.is_observers_empty:
                # Если обсерверы были в последней группе, возвращаем ошибку
                if not len(self.group_list):
                    raise ValueError("Расчет подошел к концу, но наблюдатели не пусты")
                self.group_list[-1].dq.extend(group.pop_observers())


class Group(Subject):  # Group == Definition
    def __init__(self, dq: Deque[BaseField], cm: ChainMap, variety: bool) -> None:
        self.dq = dq
        self.cm = cm
        self.parser = ParserManager()
        self.variety = variety
        super().__init__()

    def calc(self):
        while self.dq:
            current_field = self.dq.popleft()
            if current_field.formula:
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

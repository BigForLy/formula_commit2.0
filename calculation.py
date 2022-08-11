from collections import deque, ChainMap
from typing import Deque
from chain_map import DefaultListChainMap
from parser import ParserManager
from fields import BaseField
from observer import Subject


class Calculation:
    def __init__(self) -> None:
        self.cm_parent = DefaultListChainMap()
        self.group_list: Deque[Group] = deque()

    def add_group(self, dq: Deque[BaseField]):
        self.group_list.append(Group(dq, self.cm_parent.new_child()))

    def start(self):
        while self.group_list:
            group = self.group_list.popleft()
            group.calc()


class Group(Subject):
    def __init__(self, dq: Deque[BaseField], cm: ChainMap) -> None:
        self.dq = dq
        self.cm = cm
        self.parser = ParserManager()
        super().__init__()

    def calc(self):
        while self.dq:
            current_field = self.dq.popleft()
            if current_field.formula:
                current_field.update(self)
                if current_field.dependence:
                    self.attach(current_field)
            else:
                self.calculation_current_field(current_field)

    def calculation_current_field(self, current_field: "BaseField"):
        current_field.calc()
        self.cm.update({current_field.symbol: current_field.value})
        self.detach(current_field)  # type: ignore
        self.notify()

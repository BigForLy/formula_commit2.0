from collections import deque
from typing import Deque
from formula_commit.chain_map import DefaultListChainMap
from formula_commit.errors import ObserversNotEmpty
from formula_commit.fields import BaseField, NumericField
from formula_commit.fields.fields import NumericField
from formula_commit.observer import Subject
from formula_commit.consts import null


class GroupManager:
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
            current_field: BaseField = self.dq.popleft()
            current_field.check_required_field()
            if current_field.is_need_update:
                current_field.update(self)
                for item in current_field.dependence:
                    self.attach(current_field, item)
            else:
                self.calculation_current_field(current_field)

    def calculation_current_field(self, current_field: BaseField):
        current_field.calc()
        self.cm.update(
            {
                current_field.symbol: (
                    null
                    if isinstance(current_field, NumericField)
                    and current_field._value == ""
                    else current_field._value
                )
            }
        )
        self.detach(current_field)  # type: ignore
        self.notify(current_field.symbol)

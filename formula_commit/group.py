from collections import deque
from typing import Deque
from formula_commit.chain_map import DefaultListChainMap
from formula_commit.errors import ObserversNotEmpty
from formula_commit.fields import BaseField
from formula_commit.observer import Subject


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
                self.parent_group.dq.extend(group.pop_observers())

    @property
    def parent_group(self):
        """
        parent_group всегда последний в group_list
        """
        return self.group_list[-1]


class Group(Subject):  # Group == Definition
    def __init__(self, dq: Deque[BaseField], cm: DefaultListChainMap) -> None:
        self.dq: Deque[BaseField] = dq
        self.cm: DefaultListChainMap = cm
        super().__init__()

    def calc(self):
        while self.dq:
            current_field: BaseField = self.dq.popleft()
            current_field.check_required_field()
            if current_field.is_need_update:
                current_field.update(self)
            else:
                self.calculation_current_field(current_field)

        # Если родительская область видимости, то проверяем еще раз нерассчитанные поля
        # параметры которых отсутствуют в родительской области видимости
        # это может происходить при необязательном или незаполенном поле на которое указывает формула
        if not self.is_observers_empty and self.cm.is_parent:
            self.dq.extend(self.pop_observers())
            while self.dq:
                current_field: BaseField = self.dq.popleft()
                current_field.update_with_elements(self)

    def calculation_current_field(self, current_field: BaseField):
        current_field.calc()
        self.cm.update(
            {
                (
                    current_field.symbol,
                    current_field.definition_number,
                ): current_field.value
            }
        )
        # TODO: возможно объединить или вызывать внутри друг друга
        self.detach(current_field)  # type: ignore
        self.notify(current_field.symbol)

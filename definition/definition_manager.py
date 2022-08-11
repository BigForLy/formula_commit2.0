from typing import Deque, Dict, List
from calculation import Calculation
from .definition import Definition
from collections import defaultdict, deque
from chain_map import DefaultListChainMap
from fields import BaseField


class DefinitionManager:
    def __init__(self) -> None:
        self._definitions: Dict[int, Definition] = defaultdict(Definition)
        self.__fields: List[BaseField] = []
        self.deque: Deque[BaseField] = deque()
        self.cm_parent = DefaultListChainMap()

    def add_field(self, current_field: BaseField):
        definition = self._definitions[current_field.definition_number]
        definition.add_field(current_field)
        self.__fields.append(current_field)

    def separation_fields_by_definitions(self, data: list):
        for current_field in data:
            self.add_field(current_field)

    def calculation(self):
        global_deque: Deque[BaseField] = deque()
        calc = Calculation()

        for definition in self._definitions.values():
            with self.cm_parent.child() as cm:
                calc.add_group(definition.local_deque, cm)
            global_deque.extend(definition.global_deque)

        with self.cm_parent.parent() as cm:
            calc.add_group(global_deque, cm)
        calc.start()

    def get_values(self) -> dict:
        result = {}
        for current_field in self.__fields:
            result.update({current_field.primary_key: str(current_field.value)})
        return result

from typing import Dict, List
from collections import defaultdict, deque
from formula_commit.group import GroupManager
from formula_commit.chain_map import DefaultListChainMap
from formula_commit.fields import BaseField
from .definition import Definition


class DefinitionManager:
    def __init__(self) -> None:
        self._definitions: Dict[int, Definition] = defaultdict(Definition)
        self._fields: List[BaseField] = []
        self._cm_parent = DefaultListChainMap()

    def add_field(self, current_field: BaseField):
        definition = self._definitions[current_field.definition_number]
        definition.add_field(current_field)
        self._fields.append(current_field)

        self._cm_parent.elements.add(current_field.symbol)

    def separation_fields_by_definitions(self, data: list):
        for current_field in data:
            self.add_field(current_field)

    def calculation(self):
        calc = GroupManager()

        for definition in self._definitions.values():
            with self._cm_parent.child() as cm:
                calc.add_group(definition.local_deque, cm)

        # add global variables
        with self._cm_parent.parent() as cm:
            calc.add_group(deque(), cm)
        calc.start()

    def get_values(self) -> dict:
        result = {}
        for current_field in self._fields:
            result.update({current_field.primary_key: current_field.get_result_value})
        return result

from formula_commit.definition.definition_manager import DefinitionManager


class FormulaCalculation:
    def __init__(self, data) -> None:
        self.__data = data

    def calc(self):
        definition_manager = DefinitionManager()
        definition_manager.separation_fields_by_definitions(self.__data)
        definition_manager.calculation()
        return definition_manager.get_values()

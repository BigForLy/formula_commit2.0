from definition.definition_manager import DefinitionManager


class FormulaCalculation:
    def __init__(self, data) -> None:
        self.__data = data
        self.__definition_manager = DefinitionManager()

    def calc(self):
        self.__definition_manager.separation_fields_by_definitions(self.__data)
        self.__definition_manager.calculation()
        return self.__definition_manager.get_values()

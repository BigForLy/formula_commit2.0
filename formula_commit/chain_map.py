from collections import ChainMap
from typing import Any, Dict, List, Tuple
from contextlib import contextmanager
from formula_commit.consts import null


class DefaultListChainMap(ChainMap):
    """
    Превый элемент хранит значения всех остальных детей
    """

    def __setitem__(self, key, value):
        self.maps[0][key] = value
        if len(self.maps) > 1:
            mapping: Dict[str, List[Any]] = self.maps[-1]
            mapping[key].append(value)

    def __getitem__(self, key: object):
        if isinstance(key, str) and "_" in key and self.is_parent:
            symbol, definition = self.__split_into_symbol_and_definition(key)
            xs = super().__getitem__(symbol)
            if not isinstance(xs, List):
                raise ValueError(
                    "Что-то пошло не так! Ожидался список для ключа: " + key
                )
            if len(xs) < definition:
                raise ValueError(
                    "Что-то пошло не так! Значений меньше необходимого: " + key
                )
            # если значение имеет строковый тип, подставляем его представление
            result = xs[definition - 1]
            return repr(result) if isinstance(result, str) else result

        result = super().__getitem__(key)
        if isinstance(result, List) and len(result) == 1 and result[0] is null:
            return null
        # если значение имеет строковый тип, подставляем его представление
        return repr(result) if isinstance(result, str) else result

    def __contains__(self, key: object) -> bool:
        if isinstance(key, str) and "_" in key and self.is_parent:
            symbol, definition = self.__split_into_symbol_and_definition(key)
            # TODO: в глобальной области видимости все знаечения лежат в списках,
            # кроме тех полей у которых глобальная область видимости является родительской
            # у таких полей значение не список
            return any(
                symbol in m for m in self.maps[0] if len(self.maps[0][m]) >= definition
            )
        return any(key in m for m in self.maps[0])

    @staticmethod
    def __split_into_symbol_and_definition(key: str) -> Tuple[str, int]:
        try:
            symbol, definition = key.split("_")
            definition = int(definition)
        except ValueError as exc:
            raise ValueError(
                "Не удалось разделить символ и определение " + key
            ) from exc
        return symbol, definition

    @contextmanager
    def child(self):
        yield self.new_child()

    @contextmanager
    def parent(self):
        yield self

    @property
    def is_parent(self) -> bool:
        return len(self.maps) == 1

from __future__ import with_statement
from collections.abc import Iterable
from typing import Any, List, SupportsFloat, SupportsIndex, Tuple
from math import sqrt
from formula_commit.decimal_ import MDecimal
from formula_commit.consts import null


def check_nullable(func):
    """
    Проверка на наличие хотя бы одного аргумента
    """

    def _inner(self, arg=None, *args):
        if not arg:
            return null
        return func(self, arg, *args)

    return _inner


def return_first_if_once(func):
    """
    Возвращает первый аргумент, если он единственный
    """

    def _inner(self, arg=None, *args):
        if isinstance(arg, Iterable) and len(arg) == 1 and not args:
            return arg[0]
        if not isinstance(arg, Iterable) and not args:
            return arg
        return func(self, arg, *args)

    return _inner


class BaseFunc:
    def __init__(self) -> None:
        # взаимодействует со всеми определениями
        # если стоит True, всегда будет ждать значение в
        # глобальной области видимости
        self.is_global = True


class AvgFunc(BaseFunc):
    @check_nullable
    @return_first_if_once
    def __call__(self, arg: List[Any]) -> Any:
        return sum(arg) / len(arg)


class IfFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    def __call__(self, *args: Tuple[Any]) -> Any:
        assert len(args) == 3, f"Некоректная формула: {args=}"
        condition = args[0]
        return args[1] if condition else args[2]


class OnlyFunc(BaseFunc):
    def __call__(self, *args: Tuple[Any]) -> Any:
        assert len(args) == 2 or len(args) == 3, f"Некоректная формула: {args=}"
        if not args[0]:
            return null
        condition = len(set(args[0])) == 1
        success_result = args[0][0] if len(args) == 2 else args[1]
        failed_result = args[1] if len(args) == 2 else args[2]
        return success_result if condition else failed_result


class CountFunc(BaseFunc):
    @check_nullable
    def __call__(self, arg: Any) -> Any:
        return len(arg)


class IfNullFunc(BaseFunc):
    def __call__(self, first_element, second_element, *args: Any) -> Any:
        if self.__check_in_correct(first_element):
            return first_element

        if self.__check_in_correct(second_element):
            return second_element

        for element in args:
            if self.__check_in_correct(element):
                return element

        return null

    def __check_in_correct(self, element):
        return element is not None and element is not null


class CaseWhenFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False
        self.result = "if "

    def __call__(self, arg: str) -> Any:
        xs = arg.lower().split()
        is_need_append_else = True
        s = " ".join(xs)
        if s[-3:] == "end":
            s = s[:-3]
        if " else " in arg:
            is_need_append_else = False

        result = []
        # делим по "when" на условия
        for element in s.split("when"):
            # делим по "then" чтобы установить правильный порядок элементов
            list_from_element = element.split("then")
            # разворачиваем список чтобы элементы были в корректном для if порядке
            # очищаем лишние пробелы и ставим заделитель if
            element = " if ".join(x.strip() for x in reversed(list_from_element))
            result.append(element)

        result = " else ".join(result)
        if is_need_append_else:
            result = result + " else null"
        return result


class SumFunc(BaseFunc):
    @check_nullable
    @return_first_if_once
    def __call__(self, arg: Any) -> Any:
        return sum(arg)


class ReplaceFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    @check_nullable
    def __call__(self, *args: Tuple[str]) -> Any:
        assert len(args) == 3, f"Некоректная формула: {args=}"
        assert isinstance(args[0], (str, MDecimal))
        assert all(isinstance(arg, str) for arg in args[1:])
        string: str = args[0] if isinstance(args[0], str) else str(args[0])
        return string.replace(args[1], args[2])


class SqrtFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    @check_nullable
    def __call__(self, arg: SupportsFloat | SupportsIndex | MDecimal) -> Any:
        return sqrt(arg)


class MaxFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    @check_nullable
    @return_first_if_once
    def __call__(self, *args: Tuple[str]) -> Any:
        assert len(args) == 1, f"Некоректная формула: {args=}"
        return max(args[0])


class MinFunc(BaseFunc):
    def __init__(self) -> None:
        super().__init__()
        self.is_global = False

    @check_nullable
    @return_first_if_once
    def __call__(self, *args: Tuple[str]) -> Any:
        assert len(args) == 1, f"Некоректная формула: {args=}"
        return min(args[0])

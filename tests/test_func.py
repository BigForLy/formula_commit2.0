from decimal import Decimal
import pytest
from contextlib import suppress
from functions.functions import AvgFunc, IfFunc


@pytest.fixture
def avg_func():
    return AvgFunc()


class TestAvg:
    def test_empty_args(self, avg_func):
        assert (result := avg_func([])) == None, result

    def test_four_elements(self, avg_func):
        assert (result := avg_func([1, 2, 3, 4])) == 2.5, result

    def test_three_elements_incorrect(self, avg_func):  # incorrect result
        assert (result := avg_func([4, 4, 2])) == 3.3333333333333335, result

    def test_three_elements(self, avg_func):
        assert (result := avg_func([Decimal(4), Decimal(4), Decimal(2)])) == Decimal(
            "3.333333333333333333333333333"
        ), result


@pytest.fixture
def if_func():
    return IfFunc()


class TestIf:
    def test_empty_args(self, if_func):
        with suppress(AssertionError):
            assert (result := if_func([])) == None, result

    def test_less_func(self, if_func):
        assert (result := if_func(2 < 2, 2, 1)) == 1, result

    def test_less_or_equal_func(self, if_func):
        assert (result := if_func(2 <= 2, 2, 1)) == 2, result

    def test_more_func(self, if_func):
        assert (result := if_func(2 > 2, 2, 1)) == 1, result

    def test_more_or_equal_func(self, if_func):
        assert (result := if_func(2 >= 2, 2, 1)) == 2, result

    def test_equal_func(self, if_func):
        assert (result := if_func(2 == 2, 2, 1)) == 2, result

    def test_not_equal_func(self, if_func):
        assert (result := if_func(2 != 2, 2, 1)) == 1, result

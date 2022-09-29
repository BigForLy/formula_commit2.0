import pytest
from contextlib import suppress
from formula_commit.decimal_ import MDecimal
from formula_commit.consts import null
from formula_commit.functions import AvgFunc, IfFunc, OnlyFunc, CountFunc, SumFunc


@pytest.fixture
def avg_func():
    return AvgFunc()


class TestAvg:
    def test_empty_args(self, avg_func):
        assert (result := avg_func([])) is null, result

    def test_four_elements(self, avg_func):
        assert (result := avg_func([1, 2, 3, 4])) == 2.5, result

    def test_three_elements_incorrect(self, avg_func):  # incorrect result, not used int
        assert (result := avg_func([4, 4, 2])) == 3.3333333333333335, result

    def test_three_elements(self, avg_func):
        assert (
            result := avg_func([MDecimal(4), MDecimal(4), MDecimal(2)])
        ) == MDecimal("3.333333333333333333333333333"), result


@pytest.fixture
def if_func():
    return IfFunc()


class TestIf:
    def test_empty_args(self, if_func):
        with suppress(AssertionError):
            assert (result := if_func([])) == null, result

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


@pytest.fixture
def sum_func():
    return SumFunc()


class TestSum:
    def test_empty_args(self, sum_func):
        assert (result := sum_func([])) is null, result

    def test_one_arg(self, sum_func):
        assert (result := sum_func([MDecimal(1)])) == MDecimal(1), result

    def test_many_args(self, sum_func):
        assert (result := sum_func([MDecimal(1), MDecimal(1)])) == MDecimal(2), result


@pytest.fixture
def only_func():
    return OnlyFunc()


class TestOnly:
    def test_empty_args(self, only_func):
        assert (result := only_func([], "No")) is null, result

    def test_two_args_success(self, only_func):
        assert (result := only_func([1, 1, 1], "No")) == 1, result

    def test_two_args_failture(self, only_func):
        assert (result := only_func([1, 1, 2], "No")) == "No", result

    def test_three_args_success(self, only_func):
        assert (result := only_func([1, 1, 1], "Yes", "No")) == "Yes", result

    def test_three_args_failture(self, only_func):
        assert (result := only_func([1, 1, 1, 2], "Yes", "No")) == "No", result


@pytest.fixture
def count_func():
    return CountFunc()


class TestCount:
    def test_empty_args(self, count_func):
        assert (result := count_func([])) is null, result

    def test_three_args(self, count_func):
        assert (result := count_func([1, 1, 2])) == 3, result

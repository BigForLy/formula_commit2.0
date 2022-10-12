from formula_commit.components import ComponentRoundTo, ComponentContrRoundWithZero
from formula_commit.fields import NumericField
from tests.test_fields import (
    get_numeric_field,
    get_numeric_field_large_length_value,
    get_numeric_field_big_int_value,
    get_numeric_field_int_value,
)


class TestComponentRoundTo:
    def test_round_small_length_value(self, get_numeric_field: NumericField):
        ComponentRoundTo().accept(get_numeric_field)
        assert str(get_numeric_field.value) == "1.2", get_numeric_field.value

    def test_round_large_length_value(
        self, get_numeric_field_large_length_value: NumericField
    ):
        ComponentRoundTo().accept(get_numeric_field_large_length_value)
        assert (
            str(get_numeric_field_large_length_value.value) == "3.1"
        ), get_numeric_field_large_length_value.value
        assert (
            float(get_numeric_field_large_length_value.value) == 3.1
        ), get_numeric_field_large_length_value.value

    def test_round_int_value(self, get_numeric_field_int_value: NumericField):
        ComponentRoundTo().accept(get_numeric_field_int_value)
        assert (
            str(get_numeric_field_int_value.value) == "3"
        ), get_numeric_field_int_value.value
        assert (
            int(get_numeric_field_int_value.value) == 3
        ), get_numeric_field_int_value.value

    def test_round_big_int_value(self, get_numeric_field_big_int_value: NumericField):
        ComponentRoundTo().accept(get_numeric_field_big_int_value)
        assert (
            int(get_numeric_field_big_int_value.value) == 98_800
        ), get_numeric_field_big_int_value.value
        assert (
            str(get_numeric_field_big_int_value.value) == "9.88E+4"
        ), get_numeric_field_big_int_value.value


class TestComponentContrRoundWithZero:
    def test_round_small_length_value(self, get_numeric_field: NumericField):
        get_numeric_field.value = "1.20"
        ComponentContrRoundWithZero().accept(get_numeric_field)
        assert get_numeric_field.get_result_value == "1.2", get_numeric_field.value
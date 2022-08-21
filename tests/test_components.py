from components import ConcreteComponentRoundTo
from fields import NumericField
from .test_fields import (
    get_numeric_field,
    get_numeric_field_large_length_value,
    get_numeric_field_int_value,
    get_numeric_field_big_int_value,
)


class TestComponentRoundTo:
    def test_round_small_length_value(self, get_numeric_field: NumericField):
        ConcreteComponentRoundTo().accept(get_numeric_field)
        assert str(get_numeric_field._value) == "1.2", get_numeric_field._value

    def test_round_large_length_value(
        self, get_numeric_field_large_length_value: NumericField
    ):
        ConcreteComponentRoundTo().accept(get_numeric_field_large_length_value)
        assert (
            str(get_numeric_field_large_length_value._value) == "3.1"
        ), get_numeric_field_large_length_value._value
        assert (
            float(get_numeric_field_large_length_value._value) == 3.1
        ), get_numeric_field_large_length_value._value

    def test_round_int_value(self, get_numeric_field_int_value: NumericField):
        ConcreteComponentRoundTo().accept(get_numeric_field_int_value)
        assert (
            str(get_numeric_field_int_value._value) == "3"
        ), get_numeric_field_int_value._value
        assert (
            int(get_numeric_field_int_value._value) == 3
        ), get_numeric_field_int_value._value

    def test_round_big_int_value(self, get_numeric_field_big_int_value: NumericField):
        ConcreteComponentRoundTo().accept(get_numeric_field_big_int_value)
        assert (
            int(get_numeric_field_big_int_value._value) == 98_800
        ), get_numeric_field_big_int_value._value
        assert (
            str(get_numeric_field_big_int_value._value) == "9.88E+4"
        ), get_numeric_field_big_int_value._value

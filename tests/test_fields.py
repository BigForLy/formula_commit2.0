import pytest
from decimal_ import MDecimal
from fields import BoolField, NumericField


@pytest.fixture
def get_bool_field():
    return BoolField(
        definition_number=0, symbol="@a", formula="", value=1, primary_key=1
    )


@pytest.fixture
def get_numeric_field():
    return NumericField(
        symbol="@a", formula="", value="1.201", round_to=-1, primary_key=1
    )


@pytest.fixture
def get_numeric_field_large_length_value():
    return NumericField(
        symbol="@a", formula="", value=3.12121212, round_to=-1, primary_key=1
    )


@pytest.fixture
def get_numeric_field_int_value():
    return NumericField(
        symbol="@a", formula="", value=3, round_to=-3, primary_key=1
    )


@pytest.fixture
def get_numeric_field_big_int_value():
    return NumericField(
        symbol="@a", formula="", value=98_765, round_to=2, primary_key=1
    )


def test_correct_bool_field(get_bool_field: BoolField):
    assert get_bool_field.symbol == "@a"


def test_correct_numeric_value(get_numeric_field: NumericField):
    assert get_numeric_field._value == MDecimal("1.201"), get_numeric_field._value


def test_large_length_value(get_numeric_field_large_length_value: NumericField):
    assert get_numeric_field_large_length_value._value == MDecimal(
        "3.12121212"
    ), get_numeric_field_large_length_value._value

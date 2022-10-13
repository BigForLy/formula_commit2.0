import pytest
from contextlib import suppress
from formula_commit.decimal_ import MDecimal
from formula_commit.fields import BoolField, NumericField
from formula_commit.fields.fields import StringField
from formula_commit.consts import null


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
    return NumericField(symbol="@a", formula="", value=3, round_to=-3, primary_key=1)


@pytest.fixture
def get_numeric_field_big_int_value():
    return NumericField(
        symbol="@a", formula="", value=98_765, round_to=2, primary_key=1
    )


@pytest.fixture
def get_string_field():
    return StringField(
        symbol="@a", formula="", value="", round_to=2, primary_key=1, is_required=False
    )


def test_correct_bool_field(get_bool_field: BoolField):
    assert get_bool_field.symbol == "@a"


def test_correct_numeric_value(get_numeric_field: NumericField):
    assert get_numeric_field.value == MDecimal("1.201"), get_numeric_field.value


def test_large_length_value(get_numeric_field_large_length_value: NumericField):
    assert get_numeric_field_large_length_value.value == MDecimal(
        "3.12121212"
    ), get_numeric_field_large_length_value.value


def test_null_value_in_result(get_string_field: StringField):
    get_string_field.value = null
    assert get_string_field.get_result_value == "", get_string_field.get_result_value


def test_incorrect_numeric_field_value():
    """
    Проверяем, что корректно работает с разделителем ","
    """
    result = False
    with suppress(ValueError):
        NumericField(
            symbol="@a", formula="", value="3,12121212", round_to=-1, primary_key=1
        )
        result = True

    assert result, "Некорректное решение test_incorrect_numeric_field_value"

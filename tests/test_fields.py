import pytest
from decimal import Decimal
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


def test_correct_bool_field(get_bool_field: BoolField):
    assert get_bool_field.symbol == "@a"


def test_correct_numeric_value(get_numeric_field: NumericField):
    assert get_numeric_field.value == Decimal("1.201"), get_numeric_field.value

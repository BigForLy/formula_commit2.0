import pytest

from fields import BoolField


@pytest.fixture
def get_bool_field():
    return BoolField(definition_number=0, symbol="@a", formula="", value=1, primary_key=1)


def test_correct_bool_field(get_bool_field):
    assert get_bool_field.symbol == "@a"
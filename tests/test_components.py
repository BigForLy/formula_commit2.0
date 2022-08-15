from decimal import Decimal
from components import ConcreteComponentRoundTo
from fields import NumericField
from .test_fields import get_numeric_field


def test_correct_numeric_round(get_numeric_field: NumericField):
    ConcreteComponentRoundTo().accept(get_numeric_field)
    assert get_numeric_field.value == Decimal("1.2"), get_numeric_field.value

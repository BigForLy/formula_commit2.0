from fields import NumericField
from manage import FormulaCalculation


class TestCheckResult:
    def test_simple_sum(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@b", value="6", formula="", primary_key=2),
            NumericField(symbol="@c", formula="@a+@b", value="2", primary_key=3),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "6", 3: "8"}, f"Неверное решение: {result}"

    def test_simple_sum_reverse(self):
        data = [
            NumericField(symbol="@d", value="", formula="@c+2", primary_key=4),
            NumericField(symbol="@c", value="2", formula="@a+@b", primary_key=3),
            NumericField(symbol="@b", value="6", formula="", primary_key=2),
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@v", value="", formula="@d+@c", primary_key=5),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "6", 3: "8", 4:"10", 5:"18"}, f"Неверное решение: {result}"

    def test_sum_lower_number(self):
        data = [NumericField(symbol="@a", value="1.00000000000000001", formula="", primary_key=1),  # round_to='-', 
                NumericField(symbol="@b", value="1.00000000000000002", formula="", primary_key=2),
                NumericField(symbol="@c", value=2, formula="@a+@b", primary_key=3)]  # round_to='-', 
        result = FormulaCalculation(data).calc()
        assert result == {1: "1.00000000000000001", 2: "1.00000000000000002", 3: "2.00000000000000003"}, f"Неверное решение: {result}"


class TestManyDefinition:
    def test_two_definitions(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@b", value="6", formula="", primary_key=2),
            NumericField(symbol="@c", formula="@a+@b", value="2", primary_key=3),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=4),
            NumericField(symbol="@b", value="6", formula="", definition_number=1, primary_key=5),
            NumericField(symbol="@c", formula="@a+@b", value="2", definition_number=1, primary_key=6),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "6", 3: "8", 4: "3", 5: "6", 6: "9"}, f"Неверное решение: {result}"


class TestAvgFunc:
    def test_two_definitions(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=2),
            NumericField(symbol="@c", formula="avg(@a)", value="2", primary_key=3),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3", 3: "2.5"}, f"Неверное решение: {result}"

    def test_complex(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@b", value="6", formula="", primary_key=2),
            NumericField(symbol="@c", formula="@a+@b", value="2", primary_key=3),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=4),
            NumericField(symbol="@b", value="6", formula="", definition_number=1, primary_key=5),
            NumericField(symbol="@c", formula="@a+@b", value="2", definition_number=1, primary_key=6),
            NumericField(symbol="@v", formula="avg(@c)", value="", primary_key=7),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "6", 3: "8", 4: "3", 5: "6", 6: "9", 7: "8.5"}, f"Неверное решение: {result}"


class TestFieldInCommonBlock:
    def test_two_definitions(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@b", value="", formula="avg(@c)", primary_key=2),
            NumericField(symbol="@c", value="2", formula="", definition_number=1, primary_key=3),
            NumericField(symbol="@c", value="4", formula="", definition_number=2, primary_key=4),
            NumericField(symbol="@d", value="", formula="avg(@c) +   @a", primary_key=5),
            NumericField(symbol="@p", value="", formula="avg(@c) +   @b", primary_key=6),
            NumericField(symbol="@p", value="", formula="@d + @p", primary_key=7),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3", 3: "2", 4: "4", 5:"5", 6:"6", 7:"11"}, f"Неверное решение: {result}"

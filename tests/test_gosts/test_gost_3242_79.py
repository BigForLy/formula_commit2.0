from fields import StringField
from manage import FormulaCalculation


class TestGost3242_79Test:

    def test_Gost3242_79_v1(self):
        data = [
            StringField(symbol="@x", value="Отсвутствуют", formula="", primary_key="1"),
            StringField(symbol="@exp", value="", formula="@x", primary_key="2"),
            StringField(symbol="@r", value="", formula="only(@exp, 'Разногласия в оценке')", primary_key="3")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Отсвутствуют', '2': 'Отсвутствуют', '3': 'Отсвутствуют'}, f"Неверное решение: {result}"

    def test_Gost3242_79_v2(self):
        data = [
            StringField(symbol="@x", value="Присутствуют", formula="", primary_key="1"),
            StringField(symbol="@exp", value="", formula="@x", primary_key="2"),
            StringField(symbol="@r", value="", formula="only(@exp, \'Разногласия в оценке\')", primary_key="3")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Присутствуют', '2': 'Присутствуют', '3': 'Присутствуют'}, f"Неверное решение: {result}"

    def test_Gost3242_79_v3(self):
        data = [
            StringField(symbol="@x", value="Отсвутствуют", formula="", definition_number="1", primary_key="1"),
            StringField(symbol="@exp", value="", formula="@x", definition_number="1", primary_key="2"),
            StringField(symbol="@x", value="Отсвутствуют", formula="", definition_number="2", primary_key="3"),
            StringField(symbol="@exp", value="", formula="@x", definition_number="2", primary_key="4"),
            StringField(symbol="@r", value="", formula="only(@exp, \'Разногласия в оценке\')", primary_key="5")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Отсвутствуют', '2': 'Отсвутствуют', '3': 'Отсвутствуют',
                          '4': 'Отсвутствуют', '5': 'Отсвутствуют'}, f"Неверное решение: {result}"

    def test_Gost3242_79_v4(self):
        data = [
            StringField(symbol="@x", value="Отсвутствуют", formula="", definition_number="1", primary_key="1"),
            StringField(symbol="@exp", value="", formula="@x", definition_number="1", primary_key="2"),
            StringField(symbol="@x", value="Отсвутствуют1", formula="", definition_number="2", primary_key="3"),
            StringField(symbol="@exp", value="", formula="@x", definition_number="2", primary_key="4"),
            StringField(symbol="@r", value="", formula="only(@exp, \'Разногласия в оценке\')", primary_key="5")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Отсвутствуют', '2': 'Отсвутствуют', '3': 'Отсвутствуют1',
                          '4': 'Отсвутствуют1', '5': 'Разногласия в оценке'}, f"Неверное решение: {result}"

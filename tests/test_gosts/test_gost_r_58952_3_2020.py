from formula_commit.fields import NumericField, StringField
from formula_commit.manage import FormulaCalculation


class TestGostR58952_3_2020:

    def test_GostR58952_3_2020_v1(self):
        data = [
            NumericField(symbol="@mvp", round_to=-4, value=1, formula="", definition_number="1",
                         primary_key=1),
            NumericField(symbol="@mp", round_to=-4, value=2, formula="", definition_number="1",
                         formula_check="if(@mp<@mvp,'', 'Масса пластины должна быть больше массы пластины)'",
                         primary_key=2),
            NumericField(symbol="@mep", round_to=-2, value=3, formula="", definition_number="1",
                         formula_check="if(@mp<@mep,'', 'Масса пластины должна быть больше массы пластины)'",
                         primary_key=3),
            NumericField(symbol="@exp", formula='((@mvp-@mp)/(@mep-@mp))*100', round_to=-2, value="",
                         definition_number="1",
                         primary_key=4),
            StringField(symbol="@r", formula='avg(@exp)', round_to=-2, value="Отсвутствуют", primary_key=5),
            StringField(symbol="@abs_rash", formula='max(@exp)-min(@exp)', round_to=-2, value="Отсвутствуют",
                        primary_key=6)
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: '1', 2: '2', 3: '3', 4: '-100', 5: '-100', 6: '0'}, f"Неверное решение: {result}"
    
    def test_GostR58952_3_2020_v2(self):
        data = [
            NumericField(symbol="@mvp", round_to=-4, value=3, formula="", definition_number="1",
                         primary_key="1"),
            NumericField(symbol="@mp", round_to=-4, value=2, formula="", definition_number="1",
                         formula_check="if(@mp<@mvp,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="2"),
            NumericField(symbol="@mep", round_to=-2, value=3, formula="", definition_number="1",
                         formula_check="if(@mp<@mep,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="3"),
            NumericField(symbol="@exp", formula='((@mvp-@mp)/(@mep-@mp))*100', round_to=-2, value="",
                         definition_number="1",
                         primary_key="4"),
            StringField(symbol="@r", formula='avg(@exp)', round_to=-2, value="Отсвутствуют", primary_key="5"),
            StringField(symbol="@abs_rash", formula='max(@exp)-min(@exp)', round_to=-2, value="Отсвутствуют",
                        primary_key="6")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '3', '2': '2', '3': '3', '4': '100', '5': '100', '6': '0'}, f"Неверное решение: {result}"

    def test_GostR58952_3_2020_v3(self):
        data = [
            NumericField(symbol="@mvp", round_to=-4, value=3, formula = "", definition_number="1",
                         primary_key="1"),
            NumericField(symbol="@mp", round_to=-4, value=2, formula = "", definition_number="1",
                         formula_check="if(@mp<@mvp,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="2"),
            NumericField(symbol="@mep", round_to=-2, value=3, formula = "", definition_number="1",
                         formula_check="if(@mp<@mep,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="3"),
            NumericField(symbol="@exp", formula='((@mvp-@mp)/(@mep-@mp))*100', round_to=-2, value="",
                         definition_number="1", primary_key="4"),
            NumericField(symbol="@mvp", round_to=-4, value=4, formula = "", definition_number="2",
                         primary_key="5"),
            NumericField(symbol="@mp", round_to=-4, value=2, definition_number="2", formula = "",
                         formula_check="if(@mp<@mvp,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="6"),
            NumericField(symbol="@mep", round_to=-2, value=3, definition_number="2", formula = "",
                         formula_check="if(@mp<@mep,\'\', \'Масса пластины должна быть больше массы пластины)\'",
                         primary_key="7"),
            NumericField(symbol="@exp", formula='((@mvp-@mp)/(@mep-@mp))*100', round_to=-2, value="",
                         definition_number="2",
                         primary_key="8"),

            StringField(symbol="@r", formula='avg(@exp)', round_to=-2, value="Отсвутствуют", primary_key="9"),
            StringField(symbol="@abs_rash", formula='max(@exp)-min(@exp)', round_to=-2, value="Отсвутствуют",
                        primary_key="10")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': "3", '2': "2", '3': "3", '4': "100", '5': "4", '6': "2", '7': "3", '8': "200", '9': '150', '10': '100'}, f"Неверное решение: {result}"
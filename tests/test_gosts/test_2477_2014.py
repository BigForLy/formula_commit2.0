from formula_commit.fields import BoolField, NumericField, StringField
from formula_commit.manage import FormulaCalculation


class TestGost_2477_2014:

    def test_ResultFind_gost_2477_2014(self):
        data = [StringField(symbol="", formula="", value="2", primary_key="1"),
                StringField(symbol="", formula="", value="Да", primary_key="2"),

                NumericField(symbol="@V0", formula="", value="1", definition_number="1", primary_key="3"),
                NumericField(symbol="@m", formula="", value="1", definition_number="1", primary_key="4"),
                BoolField(symbol="@check_ignore", formula="", value="True", definition_number="1", primary_key="5"),
                BoolField(symbol="@input_manual", formula="", value="False", definition_number="1", primary_key="6"),
                NumericField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="1", primary_key="7"),
                NumericField(symbol="@V0", formula="", value="1", definition_number="2", primary_key="8"),
                NumericField(symbol="@m", formula="", value="1", definition_number="2", primary_key="9"),
                BoolField(symbol="@check_ignore", formula="", value="False", definition_number="2", primary_key="10"),
                BoolField(symbol="@input_manual", formula="", value="False", definition_number="2", primary_key="11"),
                NumericField(symbol="@exp", formula="(@V0/@m)*100", value="", definition_number="2", primary_key="12"),

                NumericField(symbol="@av", formula="avg(@exp)", value="", primary_key="13"),

                StringField(symbol="@r", formula="avg(@exp)", value="", primary_key="14")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '2', '2': 'Да', '3': '1', '4': '1', '5': 'True', '6': 'False', '7': '', '8': '1',
                          '9': '1', '10': 'False', '11': 'False', '12': '100', '13': '100', '14': '100'}, f"Неверное решение: {result}"

    def test_ResultFind_gost_2477_2014_all_check(self):
        data = [StringField(symbol="", formula="", value="2", primary_key="1"),
                StringField(symbol="", formula="", value="Да", primary_key="2"),

                NumericField(symbol="@V0", formula="", value="1", definition_number="1", primary_key="3"),
                NumericField(symbol="@m", formula="", value="1", definition_number="1", primary_key="4"),
                BoolField(symbol="@check_ignore", formula="", value="True", definition_number="1", primary_key="5"),
                BoolField(symbol="@input_manual", formula="", value="False", definition_number="1", primary_key="6"),
                NumericField(symbol="@exp", formula="(@V0/@m)*100", value="7", definition_number="1", primary_key="7"),
                NumericField(symbol="@V0", formula="", value="1", definition_number="2", primary_key="8"),
                NumericField(symbol="@m", formula="", value="1", definition_number="2", primary_key="9"),
                BoolField(symbol="@check_ignore", formula="", value="True", definition_number="2", primary_key="10"),
                BoolField(symbol="@input_manual", formula="", value="False", definition_number="2", primary_key="11"),
                NumericField(symbol="@exp", formula="(@V0/@m)*100", value="8", definition_number="2", primary_key="12"),

                NumericField(symbol="@av", formula="avg(@exp)", value="", primary_key="13"),

                StringField(symbol="@r", formula="avg(@exp)", value="", primary_key="14")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '2', '2': 'Да', '3': '1', '4': '1', '5': 'True', '6': 'False', '7': '7', '8': '1',
                          '9': '1', '10': 'True', '11': 'False', '12': '8', '13': 'null', '14': 'null'}, f"Неверное решение: {result}"
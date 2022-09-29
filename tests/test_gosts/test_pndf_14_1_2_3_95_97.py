from formula_commit.fields import NumericField, StringField, BoolField
from formula_commit.manage import FormulaCalculation


class TestPNDF14_1_2_3_95_97:

    def test_PNDF14_1_2_3_95_97(self):
        data = [
            NumericField(symbol="@ctr", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="1",
                         primary_key="1"),
            NumericField(symbol="@vtr", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="1",
                         primary_key="2"),
            NumericField(symbol="@v", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="1",
                         primary_key="3"),
            NumericField(symbol="@qq", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="1",
                         primary_key="4"),
            BoolField(symbol="@check_ignore", value="False", formula="", definition_number="1", primary_key="5"),
            BoolField(symbol="@input_manual", value="True", formula="", definition_number="1", primary_key="6"),
            NumericField(symbol="@exp", round_to=-3, round_with_zeros=False, definition_number="1",
                         formula="if(@qq='Используется',1.25*40.08*1000*(@ctr*@vtr)/@v,if(@qq='Не используется',40.08*1000*(@ctr*@vtr)/@v,null*null))",
                         value=1,
                         primary_key="7"),

            NumericField(symbol="@ctr", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="2",
                         primary_key="8"),
            NumericField(symbol="@vtr", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="2",
                         primary_key="9"),
            NumericField(symbol="@v", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="2",
                         primary_key="10"),
            NumericField(symbol="@qq", round_to=-3, value="", formula="", round_with_zeros=False, definition_number="2",
                         primary_key="11"),
            BoolField(symbol="@check_ignore", value="False", formula="", definition_number="2", primary_key="12"),
            BoolField(symbol="@input_manual", value="True", formula="", definition_number="2", primary_key="13"),
            NumericField(symbol="@exp", round_to=-3, round_with_zeros=False, definition_number="2",
                         formula="if(@qq='Используется',1.25*40.08*1000*(@ctr*@vtr)/@v,if(@qq='Не используется',40.08*1000*(@ctr*@vtr)/@v,null))",
                         value=1,
                         primary_key="14"),

            StringField(symbol="@pogr",
                        formula="if(avg(@exp)>=1 and avg(@exp)<=2,0.25*avg(@exp),if(avg(@exp)>2 and avg(@exp)<=10,0.15*avg(@exp),if(avg(@exp)>10 and avg(@exp)<=2000,0.11*avg(@exp),null)))",
                        value="",
                        primary_key="15"),
            StringField(symbol="@r",
                        formula="IF (avg(@exp)<1,'<1' ,IF (avg(@exp)>1000,'>1000',REPLACE(AVG(@exp),'.',',')))",
                        value="1.0",
                        primary_key="16"),
            StringField(symbol="@povt",
                        formula="if(avg(@exp)>=1 and avg(@exp)<=2,22,if(avg(@exp)>2 and avg(@exp)<=10,14,if(avg(@exp)>10 and avg(@exp)<=2000,6,null)))",
                        value="22",
                        primary_key="17"),
            StringField(symbol="@abs_rash",
                        formula="200*(max(@exp)-min(@exp))/(max(@exp)+min(@exp))",
                        value="0",
                        primary_key="18"),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '', '2': '', '3': '', '4': '', '5': '0', '6': '1', '7': '1',
                          '8': '', '9': '', '10': '', '11': '', '12': '0', '13': '1',
                          '14': '1', '15': '0.25', '16': '1', '17': '22', '18': '0'}, result

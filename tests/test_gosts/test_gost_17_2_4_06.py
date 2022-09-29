from formula_commit.fields import BoolField, StringField, NumericField
from formula_commit.manage import FormulaCalculation


class TestGost_17_2_4_06:
    def test_gost_17_2_4_06_v1(self):
        data = [NumericField(symbol="@densityAir", formula="1.293", value="1.293", round_to=-3, definition_number="1",
                             primary_key="1"),
                NumericField(symbol="@absHumidity", round_to=-1, formula="", value="1.6", definition_number="1", primary_key="2"),
                NumericField(symbol="@tGas", round_to=-2, formula="", value="15.3", definition_number="1", primary_key="3"),
                NumericField(symbol="@pAtmo", round_to=-2, formula="", value="98.8", definition_number="1", primary_key="4"),
                NumericField(symbol="@Pd", round_to=-2, formula="", value="228.16", definition_number="1", primary_key="5"),
                NumericField(symbol="@pStat", round_to=-2, formula="", value="813.61", definition_number="1", primary_key="6"),
                NumericField(symbol="@exp", round_to=-2, formula="SQRT(2*@Pd/@densityWork)", value="",
                             definition_number="1", primary_key="7"),
                NumericField(symbol="@concentrationWater", round_to=-5,
                             formula="round(((@densityAir*@absHumidity)/1000),5)", value="0.00207",
                             definition_number="1", primary_key="8"),
                NumericField(symbol="@densityGas", round_to=-5,
                             formula="round((@densityAir+@concentrationWater)/(1+1.244*@concentrationWater),3)",
                             value="1.292", definition_number="1", primary_key="9"),
                NumericField(symbol="@densityWork", round_to=-3,
                             formula="round((2.695*@densityGas*(@pAtmo+@pStat/1000)/(273+@tGas)),3)", value="1.203",
                             definition_number="1", primary_key="10"),
                StringField(symbol="@X", formula="avg(@exp)", value="19.48", primary_key="11")
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1.293', '2': '1.6', '3': '15.3', '4': '98.8', '5': '228.16', '6': '813.61', '7': '19.48',
                          '8': '0.00207',
                          '9': '1.292', '10': '1.203', '11': '19.48'}, \
            "Неверное решение ГОСТ 17.2.4.06-90"

    def test_gost_17_2_4_06_v2(self):
        data = [NumericField(symbol="@v", formula="", value=20.25, round_to=-2, definition_number="1",
                             primary_key="1"),
                NumericField(symbol="@pStat", round_to=-2, formula="", value=-1008, definition_number="1", primary_key="2"),
                NumericField(symbol="@pAtmo", round_to=-2, formula="", value=98.9, definition_number="1", primary_key="3"),
                NumericField(symbol="@tGas", round_to=-2, formula="", value=19.1, definition_number="1", primary_key="4"),
                StringField(symbol="@sRectangle", round_to=-4,
                            formula="(case when @flueLength>0 then REPLACE (round(CAST(@flueLength*@width/1000000 as DECIMAL(15,4)),4),'.',',') else REPLACE ('-','.',',')end)",
                            value="-", definition_number="1", primary_key="5"),
                NumericField(symbol="@flueLength", round_to=-2,
                             formula="", value="", definition_number="1", primary_key="6"),
                StringField(symbol="@sRound", round_to=-4,
                            formula="(case when @diameter>0 then REPLACE(round(CAST((3.14*(@diameter*@diameter))/(4000000)as DECIMAL(15,4)),4),'.',',')else REPLACE ('-','.',',')end)",
                            value="0.1590", definition_number="1", primary_key="7"),
                NumericField(symbol="@x2", round_to=-5,
                             formula="round(2.695*@x*(@pAtmo+@pStat/1000)/(273+@tGas),3)",
                             value=2.908, definition_number="1", primary_key="8"),
                StringField(symbol="@diameter",
                            formula="(case when @d>0 then REPLACE (@d-@h,'.',',')else REPLACE ('-','.',',')end)",
                            value="450", round_to=-2, definition_number="1",
                            primary_key="9"),
                BoolField(symbol="@input_manual", formula="", value="True", definition_number="1", primary_key="10"),
                StringField(symbol="@x", round_to=-5,
                            formula="(case when @sRectangle>0 then REPLACE (round((@v*@sRectangle),3),'.',',')else REPLACE (round((@v*@sRound),3),'.',',')end)",
                            value="3.220", definition_number="1", primary_key="11"),
                NumericField(symbol="@d", formula="", value=470, round_to=-2, definition_number="1",
                             primary_key="12"),
                NumericField(symbol="@width", formula="", value="", round_to=-2, definition_number="1", required_field=False,
                             primary_key="13"),
                NumericField(symbol="@h", formula="", value=20, round_to=-2, definition_number="1",
                             primary_key="14"),

                StringField(symbol="@exp", formula="avg(@x)", value="", round_to=-3, round_with_zeros=True,
                            primary_key="15"),
                StringField(symbol="@abs_pogr", formula="max(@x)-min(@x)", round_to=-1, value="0,0",
                            primary_key="16"),
                StringField(symbol="@exp2", formula="avg(@x2)", value="", round_to=-3, primary_key="17"),
                StringField(symbol="@abs_pogr2", formula="max(@x2)-min(@x2)", round_to=-1, value="0,0",
                            primary_key="18"),
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '20.25', '2': '-1008', '3': '98.9', '4': '19.1', '5': '-', '6': '', '7': '0.1590',
                          '8': '2.908', '9': '450', '10': '1', '11': '3.220', '12': '470', '13': '', '14': '20',
                          '15': '3.220', '16': '0.0', '17': 'null', '18': 'null'}, \
            "Неверное решение ГОСТ 17.2.4.06-90"
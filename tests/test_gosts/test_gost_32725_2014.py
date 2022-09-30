from formula_commit import (
    NumericField,
    BoolField,
    StringField,
    FormulaCalculation,
)


class TestGostR58952_3_2020:
    def test_v1(self):
        data = [
            NumericField(
                symbol="@m",
                round_to=-2,
                value=2,
                formula="",
                definition_number="1",
                formula_check="if(@m>0,'','Масса мерной пробы до начала мокрого просеивания должна быть больше 0')",
                primary_key=1,
            ),
            NumericField(
                symbol="@exp",
                round_to=-1,
                value=2,
                formula="(@m-@m1)/@m*100",
                definition_number="1",
                formula_check="if(@exp>0,'','Результат определения должен быть больше 0')",
                primary_key=2,
            ),
            NumericField(
                symbol="@m1",
                round_to=-2,
                value=1,
                formula="",
                definition_number="1",
                formula_check="if(@m>@m1,if(@m1>0,'','Масса после высушивания должна быть больше 0'),if(@m1>0,'Масса после высушивания должна быть меньше массы до начала просеивания ','Масса после высушивания должна быть меньше массы до начала просеивания и быть больше 0'))",
                primary_key=3,
            ),
            StringField(
                symbol="", value="", formula="avg(@exp)", round_to=-2, primary_key=4
            ),
            StringField(symbol="r", value="", formula="", round_to=-2, primary_key=5),
            StringField(
                symbol="",
                value="",
                formula="max(@exp)-min(@exp)",
                round_to=-2,
                primary_key=6,
            ),
            StringField(symbol="", value="", formula="", round_to=0, primary_key=7),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {
            1: "2",
            2: "50.0",
            3: "1",
            4: "50.0",
            5: "",
            6: "0.0",
            7: "",
        }, f"Неверное решение: {result}"

    def test_v2(self):
        data = [
            StringField(
                symbol="",
                value="И.А. Ахметова",
                formula="",
                round_to=0,
                primary_key=1,
            ),
            StringField(
                symbol="",
                value="02.02.2022 14:16:38",
                formula="",
                round_to=0,
                primary_key=2,
            ),
            BoolField(
                symbol="check_ignore",
                value=0,
                definition_number=1,
                formula="",
                primary_key=3,
            ),
            BoolField(
                symbol="input_manual",
                value=0,
                definition_number=1,
                formula="",
                primary_key=4,
            ),
            NumericField(
                symbol="m",
                round_to=-2,
                value=1000,
                formula="",
                definition_number=1,
                primary_key=5,
            ),
            NumericField(
                symbol="m1",
                round_to=-2,
                value=978,
                formula="",
                definition_number=1,
                primary_key=6,
            ),
            NumericField(
                symbol="exp",
                round_to=-1,
                value=2.2,
                formula="(@m-@m1)/@m*100",
                definition_number=1,
                primary_key=7,
            ),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {
            1: "И.А. Ахметова",
            2: "02.02.2022 14:16:38",
            3: "0",
            4: "0",
            5: "1000",
            6: "978",
            7: "2.2",
        }, f"Неверное решение: {result}"

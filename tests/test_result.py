import time
from contextlib import suppress
from memory_profiler import profile
from formula_commit.fields import BoolField, NumericField, StringField
from formula_commit.manage import FormulaCalculation
from formula_commit.errors import ObserversNotEmpty


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
    
    def test_two_definitions_and_field(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@b", value="4", formula="", primary_key=2),
            NumericField(symbol="@c", value="", formula="avg(@a)+@b", primary_key=3),
            NumericField(symbol="@a", value="3", formula="", definition_number=1 ,primary_key=4),
            NumericField(symbol="@b", value="5", formula="", definition_number=1, primary_key=5),
            NumericField(symbol="@c", value="", formula="avg(@a)+@b", definition_number=1, primary_key=6),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "4", 3: "6.5", 4:"3", 5:"5", 6:"7.5"}, f"Неверное решение: {result}"

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


class TestIfFunc:
    def test_one_definitions_true(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@c", value="2", formula="if(   @a=2,3,4)", primary_key=2),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3"}, f"Неверное решение: {result}"

    def test_one_definitions_false(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@c", value="2", formula="if(   @a<>2,3,4)", primary_key=2),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "4"}, f"Неверное решение: {result}"

    def test_two_definitions(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@c", value="2", formula="if(   @a=2,3,4)", primary_key=2),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=3),
            NumericField(symbol="@c", value="2", formula="if(   @a=2,3,4)", definition_number=1, primary_key=4),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3", 3: "3", 4: "4"}, f"Неверное решение: {result}"

    def test_complex_avg_and_if_false(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=2),
            NumericField(symbol="@c", value="2", formula="if(   avg(@a)=2,3,4)", definition_number=1, primary_key=3),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3", 3: "4"}, f"Неверное решение: {result}"

    def test_complex_avg_and_if_true(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),
            NumericField(symbol="@a", value="3", formula="", definition_number=1, primary_key=2),
            NumericField(symbol="@c", value="2", formula="if(   avg(@a)=2.5,3,4)", definition_number=1, primary_key=3),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "2", 2: "3", 3: "3"}, f"Неверное решение: {result}"

    def test_formula_v1(self):
        formula = ("if_(MDecimal('47.853') is not null and MDecimal('47.853')>=MDecimal('47.396') and "
        "(MDecimal('47.853')<=MDecimal('48.530') or MDecimal('48.530') is null or MDecimal('48.530')=MDecimal('47.396')) and "
        "(MDecimal('47.853')<=MDecimal('48.083') or MDecimal('48.083') is null or MDecimal('48.083')=MDecimal('47.396')) and "
        "(MDecimal('47.853')<=MDecimal('48.069') or MDecimal('48.069') is null or MDecimal('48.069')=MDecimal('47.396')) and "
        "(MDecimal('47.853')<=MDecimal('47.901') or MDecimal('47.901') is null or MDecimal('47.901')=MDecimal('47.396')) and "
        "(MDecimal('47.853')<=MDecimal('47.396') or MDecimal('47.396') is null or MDecimal('47.396')=MDecimal('47.396')),"
        "MDecimal('47.853'),null) ")
        data = [
            NumericField(symbol="@iexp", formula=formula, value="1", round_to=-1, primary_key=1),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "47.9"}, f"Неверное решение: {result}"

    def test_formula_v2(self):
        formula=("if_(MDecimal('48.069') is not null and MDecimal('48.069')>=MDecimal('47.396') and "
        "(MDecimal('48.069')<=MDecimal('48.530') or MDecimal('48.530') is null or MDecimal('48.530')=MDecimal('47.396')) and "
        "(MDecimal('48.069')<=MDecimal('48.083') or MDecimal('48.083') is null or MDecimal('48.083')=MDecimal('47.396')) and "
        "(MDecimal('48.069')<=MDecimal('47.853') or MDecimal('47.853') is null or MDecimal('47.853')=MDecimal('47.396')) and "
        "(MDecimal('48.069')<=MDecimal('47.901') or MDecimal('47.901') is null or MDecimal('47.901')=MDecimal('47.396')) and "
        "(MDecimal('48.069')<=MDecimal('47.396') or MDecimal('47.396') is null or MDecimal('47.396')=MDecimal('47.396')),"
        "MDecimal('48.069'),null) ")
        data = [
            NumericField(symbol="@iexp", formula=formula, value="1", round_to=-1, primary_key=1),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "null"}, f"Неверное решение: {result}"
    
    def test_formula_v3(self):
        formula = (
            "IF(@iexp_1 is not null AND @iexp_1>=@minexp AND\r\n"
            "(@iexp_1<=@iexp_2 OR @iexp_2 is null OR @iexp_2=@minexp) AND\r\n"
            "(@iexp_1<=@iexp_3 OR @iexp_3 is null OR @iexp_3=@minexp) AND\r\n"
            "(@iexp_1<=@iexp_4 OR @iexp_4 is null OR @iexp_4=@minexp) AND\r\n"
            "(@iexp_1<=@iexp_5 OR @iexp_5 is null OR @iexp_5=@minexp) AND\r\n"
            "(@iexp_1<=@iexp_6 OR @iexp_6 is null OR @iexp_6=@minexp),@iexp_1,null)\r\n"
        )
        data = [
            NumericField(symbol="@iexp_1", formula="", value="1", round_to=-1, primary_key=1),
            NumericField(symbol="@iexp_2", formula="", value="1", round_to=-1, primary_key=2),
            NumericField(symbol="@iexp_3", formula="", value="1", round_to=-1, primary_key=3),
            NumericField(symbol="@iexp_4", formula="", value="1", round_to=-1, primary_key=4),
            NumericField(symbol="@iexp_5", formula="", value="1", round_to=-1, primary_key=5),
            NumericField(symbol="@iexp_6", formula="", value="1", round_to=-1, primary_key=6),
            NumericField(symbol="@minexp", formula="", value="1", round_to=-1, primary_key=7),
            NumericField(symbol="@a", formula=formula, value="1", round_to=-1, primary_key=8),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "1", 2: "1", 3: "1", 4: "1", 5: "1", 6: "1", 7: "1", 8: "1"}, f"Неверное решение: {result}"
    
    def test_formula_order_incorrect(self):
        data = [
            NumericField(symbol="@iexp", formula="", value="4", round_to=-1, definition_number=4, primary_key=1),
            NumericField(symbol="@iexp", formula="", value="2", round_to=-1, definition_number=2, primary_key=2),
            NumericField(symbol="@iexp", formula="", value="3", round_to=-1, definition_number=3, primary_key=3),
            NumericField(symbol="@iexp", formula="", value="1", round_to=-1, definition_number=1, primary_key=4),
            NumericField(symbol="@iexp", formula="", value="6", round_to=-1, definition_number=6, primary_key=5),
            NumericField(symbol="@iexp", formula="", value="5", round_to=-1, definition_number=5, primary_key=6),
            NumericField(symbol="@a", formula="@iexp_4", value="4", round_to=-1, primary_key=7),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "4", 2: "2", 3: "3", 4: "1", 5: "6", 6: "5", 7: "4"}, f"Неверное решение: {result}"

    def test_formula_v4(self):
        data = [
            NumericField(symbol="@minexp", formula="", value="1", definition_number=1, round_to=-1, primary_key=1),
            NumericField(symbol="@a", formula="if(@minexp_1 is not null, 1, 2)", value="", round_to=-1, primary_key=2),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "1", 2: "1"}, f"Неверное решение: {result}"

    def test_formula_v5(self):
        data = [
            NumericField(symbol="@q", formula="@b", value="1", round_to=-1, primary_key=1),
            NumericField(symbol="@minexp", formula="", value="1", round_to=-1, definition_number=1, primary_key=2),
            NumericField(symbol="@a", formula="if(@minexp_1 is not null, 1, 2)", value="", round_to=-1, primary_key=3),
            NumericField(symbol="@b", formula="@a", value="", round_to=-1, primary_key=4),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "1", 2: "1", 3: "1", 4: "1"}, f"Неверное решение: {result}"

    def test_formula_v6(self):
        data = [
            NumericField(symbol="@ign", formula="", value="", round_to=-1, definition_number=1, is_required=False, primary_key=1),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@exp)\r\n", definition_number=1, value="", round_to=-1, primary_key=2),
            NumericField(symbol="@exp", formula="", value="1", round_to=-1, definition_number=1, primary_key=3),
            NumericField(symbol="@ign", formula="", value="", round_to=-1, definition_number=2, is_required=False, primary_key=4),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@exp)\r\n", definition_number=2, value="", round_to=-1, primary_key=5),
            NumericField(symbol="@exp", formula="", value="1", round_to=-1, definition_number=2, primary_key=6),
            NumericField(symbol="@p", formula="avg(@b)", value="1", round_to=-1, definition_number=2, primary_key=7),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "", 2: "1", 3: "1", 4: "", 5: "1", 6: "1", 7: "1"}, f"Неверное решение: {result}"
        

class TestFieldInCommonBlock:
    @profile(precision=4)
    def test_two_definitions(self):
        data = [
            NumericField(symbol="@a", value="2", formula="", primary_key=1),  # common block
            NumericField(symbol="@b", value="", formula="avg(@c)", primary_key=2),  # common block
            NumericField(symbol="@c", value="2", formula="", definition_number=1, primary_key=3),  # assay block
            NumericField(symbol="@c", value="4", formula="", definition_number=2, primary_key=4),  # assay block
            NumericField(symbol="@d", value="", formula="avg(@c) +   @a", primary_key=5),  # common block
            NumericField(symbol="@p", value="", formula="avg(@c) +   @b", primary_key=6),  # common block
            NumericField(symbol="@o", value="", formula="@d + @p", primary_key=7),  # common block
        ]
        start_time = time.time()
        result = FormulaCalculation(data).calc()
        print(f"Время: {time.time()-start_time}")
        assert result == {1: "2", 2: "3", 3: "2", 4: "4", 5:"5", 6:"6", 7:"11"}, f"Неверное решение: {result}"


class TestAllFieldsCheckIgnore:
    def test_ResultFind_gost_2477_2014_all_check(self):
        data = [NumericField(symbol="@m", value="1", definition_number="1", formula="", primary_key="1"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", formula="", primary_key="2"),
                BoolField(symbol="@input_manual", value="False", definition_number="1", formula="", primary_key="3"),
                NumericField(symbol="@m", value="1", definition_number="2", formula="", primary_key="4"),
                BoolField(symbol="@check_ignore", value="True", definition_number="2", formula="", primary_key="5"),
                BoolField(symbol="@input_manual", value="False", definition_number="2", formula="", primary_key="6"),

                NumericField(symbol="@av", formula="avg(@m)", value="", primary_key="7")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1', '2': 'True', '3': 'False', 
                          '4': '1', '5': 'True', '6': 'False', '7': 'null'}, f"Неверное решение: {result}"


class TestIncorrectFormula:
    def test_empty_list(self):
        data = [NumericField(symbol="@m", value="1", definition_number="1", formula="", primary_key="1"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", formula="", primary_key="2"),

                NumericField(symbol="@av", formula="@m", value="", primary_key="3"),
                NumericField(symbol="@av2", formula="@av+1", value="", primary_key="4")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1', '2': 'True', '3': 'null', '4': 'null'}, f"Неверное решение: {result}"

    def test_not_field_in_formula(self):
        data = [NumericField(symbol="@m", value="1", definition_number="1", formula="", primary_key="1"),

                NumericField(symbol="@av", formula="@m+@d", value="", primary_key="2")]
        result = None
        with suppress(ObserversNotEmpty):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_null_in_if(self):
        data = [NumericField(symbol="@m", value="1", definition_number="1", formula="", primary_key="1"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", formula="", primary_key="2"),

                NumericField(symbol="@av", formula="if(avg(@m) < 2, 1,2)", value="", primary_key="3")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1', '2': 'True', '3': '2'}, f"Неверное решение: {result}"

    def test_null_equal(self):
        data = [NumericField(symbol="@m", value="1", definition_number="1", formula="", primary_key="1"),
                BoolField(symbol="@check_ignore", value="True", definition_number="1", formula="", primary_key="2"),

                NumericField(symbol="@av", formula="if(@m <> 2, 1,2)", value="", primary_key="3")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1', '2': 'True', '3': '2'}, f"Неверное решение: {result}"

    def test_empty_value_in_required_fields(self):
        data = [NumericField(symbol="@m", value="", definition_number="1", formula="", primary_key="1"),

                NumericField(symbol="@av", formula="@m-1", value="", primary_key="2")]
        result = None
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_empty_value_in_calc(self):
        data = [NumericField(symbol="@m", value="", definition_number="1", formula="", is_required=False, primary_key="1"),

                NumericField(symbol="@av", formula="@m-1", value="", primary_key="2")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '', '2': 'null'}, f"Неверное решение: {result}"

    def test_no_required_field(self):
        result = None
        data = [NumericField(symbol="@m", value="", definition_number="1", formula="", primary_key="1"),

                NumericField(symbol="@av", formula="@m-1", value="", primary_key="2")]
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_local_global_fomula(self):
        result = None
        data = [NumericField(symbol="@m", value="1", formula="", primary_key="1"),

                NumericField(symbol="@av", formula="avg(@m)", value="", primary_key="2"),

                NumericField(symbol="@ab", formula="avg(@av)", value="", primary_key="3")]
        result = FormulaCalculation(data).calc()
        assert result == {'1': '1', '2': '1', '3': '1'}, f"Неверное решение: {result}"

    def test_str_in_formula_in_formula(self):
        data = [
            StringField(symbol="@x", value="Отсвутствуют", formula="", primary_key="1"),
            StringField(symbol="@exp", value="", formula="@x", primary_key="2"),
            StringField(symbol="@r", value="", formula="if(@exp <> '', @exp, 'Н')", primary_key="3")
        ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': "Отсвутствуют", '2': 'Отсвутствуют', '3': 'Отсвутствуют'}, f"Неверное решение: {result}"

    def test_formula_v1(self):
        formula = (
            "(case when null<=2 then null\r\n"
            "when null<6 AND null>2 then (null-@minexp)/(null-1)\r\n"
            "when null>=6 then (null-@minexp-null)/(null-2) end)\r\n"
        )
        data = [
            NumericField(symbol="@minexp", formula="", value="1", round_to=-1, primary_key=1),
            NumericField(symbol="@a", formula=formula, value="1", round_to=-1, primary_key=2),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "1", 2: "null"}, f"Неверное решение: {result}"

    def test_formula_null_div(self):
        """
        Деление на null
        """
        data = [
            NumericField(symbol="@minexp", formula="100*MDecimal('60.0')/null", value="", round_to=-1, primary_key=1),
            NumericField(symbol="@a", formula="@minexp", value="", round_to=-1, primary_key=2),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "null", 2: "null"}, f"Неверное решение: {result}"

    def test_formula_zero_div(self):
        """
        Деление на 0
        """
        data = [
            NumericField(symbol="@minexp", formula="100*MDecimal('60.0')/MDecimal('0.0')", value="", round_to=-1, primary_key=1),
        ]
        result = None
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_formula_min_method(self):
        """
        Проверка функции Min
        """
        data = [
            NumericField(symbol="@p", formula="min(@b)", value="0", round_to=-1, definition_number=2, primary_key=1),
            NumericField(symbol="@b", formula="", definition_number=1, value="1", round_to=-1, primary_key=2),
            NumericField(symbol="@b", formula="", definition_number=2, value="2", round_to=-1, primary_key=3),
            NumericField(symbol="@b", formula="", definition_number=3, value="3", round_to=-1, primary_key=4),
            NumericField(symbol="@b", formula="", definition_number=4, value="4", round_to=-1, primary_key=5),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: "1", 2: "1", 3: "2", 4: "3", 5: "4"}, f"Неверное решение: {result}"

    def test_the_formula_itself_v1(self):
        # TODO: если ссылка на самого себя и значение не заполено что вывести? null/""? но у поля numeric не должно быть ""
        data = [
            NumericField(symbol="@ign", formula="", value="", round_to=-1, definition_number=1, is_required=False, primary_key=1),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@b)\r\n", definition_number=1, value="", round_to=-1, primary_key=2),
            NumericField(symbol="@ign", formula="", value="", round_to=-1, definition_number=2, is_required=False, primary_key=3),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@b)\r\n", definition_number=2, value="", round_to=-1, primary_key=4),
            NumericField(symbol="@p", formula="avg(@b)", value="1", round_to=-1, definition_number=2, primary_key=5),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: '', 2: 'null', 3: '', 4: 'null', 5: 'null'}, f"Неверное решение: {result}"

    def test_the_formula_itself_v2(self):
        data = [
            NumericField(symbol="@ign", formula="", value="50", round_to=-1, definition_number=1, primary_key=1),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@b)\r\n", value="5", definition_number=1, round_to=-1, primary_key=2),
            NumericField(symbol="@ign", formula="", value="60", round_to=-1, definition_number=2, primary_key=3),
            NumericField(symbol="@b", formula="if(@ign = 'Не учитывать',null,@b)\r\n", value="6", definition_number=2, round_to=-1, primary_key=4),
            NumericField(symbol="@p", formula="avg(@b)", value="1", round_to=-1, definition_number=2, primary_key=5),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: '50', 2: '5', 3: '60', 4: '6', 5: '5.5'}, f"Неверное решение: {result}"

    def test_the_formula_rounding(self):
        formula = "if_((10*MDecimal('1')*MDecimal('0.95')*MDecimal('510.84')/MDecimal('100')) is null,MDecimal('48.53'),(10*MDecimal('1')*MDecimal('0.95')*MDecimal('510.84')/MDecimal('100'))) "
        data = [
            NumericField(symbol="@ign", formula=formula, value="50", round_to=-3, round_with_zeros=False, definition_number=1, primary_key=1),
        ]
        result = FormulaCalculation(data).calc()
        assert result == {1: '48.53'}, f"Неверное решение: {result}"


class TestOnlyResult:
    def test_1param_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Привет', '2': 'Привет', '3': 'Привет'}, f"Неверное решение: {result}"

    def test_1param_not_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет1", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Привет', '2': 'Привет1', '3': 'Разногласие по параметрам'}, f"Неверное решение: {result}"

    def test_2param_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "ПП", "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Привет', '2': 'Привет', '3': 'ПП'}, f"Неверное решение: {result}"

    def test_2param_not_equals(self):
        data = [StringField(symbol="@t", formula="", value="Привет", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="", value="Привет1", definition_number="2", primary_key="2"),
                StringField(symbol="@exp", formula='only(@t, "ПП", "Разногласие по параметрам")', value="500",
                            definition_number="1", primary_key="3")
                ]
        result = FormulaCalculation(data).calc()
        assert result == {'1': 'Привет', '2': 'Привет1', '3': 'Разногласие по параметрам'}, f"Неверное решение: {result}"


class TestEval:
    def test_os(self):
        data = [NumericField(symbol="@b", formula="", value="4", definition_number="1", primary_key="1"),
                NumericField(symbol="@t", formula="@b + os.cpu_count()", value="4", definition_number="1", primary_key="2")]
        result = None
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_os_string(self):
        data = [NumericField(symbol="@b", formula="", value="4", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="@b + os.cpu_count()", value="4", definition_number="1", primary_key="2")]
        result = None
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

    def test_result_fields_value_zero(self):
        data = [NumericField(symbol="@a", formula="", value="0,0000", round_to=-4, primary_key=1, is_round_with_zeros=True)]
        result = FormulaCalculation(data).calc()
        assert result == {1: "0.0000"}, f"Неверное решение: {result}"


    def test_import(self):
        data = [NumericField(symbol="@b", formula="", value="4", definition_number="1", primary_key="1"),
                StringField(symbol="@t", formula="@b + __import__('os').cpu_count()", value="Привет", definition_number="1", primary_key="2")]
        result = None
        with suppress(ValueError):
            result = FormulaCalculation(data).calc()
        assert result == None, f"Неверное решение: {result}"

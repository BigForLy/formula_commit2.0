from formula_commit.calculation import calculation
from formula_commit.consts import null
from formula_commit.functions import FUNC_CALLABLE


def test_case_when_1():
    formula = (
        "case_when(\" 0.8*null is null then null when 0.8*null>=120 then 'B120' when 0.8*null>=110 then 'B110' "
        "when 0.8*null>=100 then 'B100' when 0.8*null>=90 then 'B90' when 0.8*null>=80 then 'B80' "
        "when 0.8*null>=70 then 'B70' when 0.8*null>=60 then 'B60' when 0.8*null>=55 then 'B55' when 0.8*null>=50 then 'B50' "
        "when 0.8*null>=45 then 'B45' when 0.8*null>=40 then 'B40' when 0.8*null>=35 then 'B35' when 0.8*null>=30 then 'B30' "
        "when 0.8*null>=27.5 then 'B27,5' when 0.8*null>=25 then 'B25' when 0.8*null>=22.5 then 'B22,5' when 0.8*null>=20 then 'B20' "
        "when 0.8*null>=15 then 'B15' when 0.8*null>=12.5 then 'B12,5' when 0.8*null>=10 then 'B10' when 0.8*null>=7.5 then 'B7,5' "
        "when 0.8*null>=5 then 'B5' when 0.8*null>=3.5 then 'B3,5' else 'не определён' end\")  "
    )
    assert (result := calculation(formula, case_when=FUNC_CALLABLE["case_when"])) is null, result

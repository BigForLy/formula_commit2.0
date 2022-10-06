import pytest

from formula_commit.parser import ParserManager


@pytest.fixture
def parser() -> ParserManager:
    return ParserManager()


class TestParser:
    def test_avg_local(self, parser: ParserManager):
        assert (
            "".join(parser.replace("avg(((@a))) + @a", "@a", "3", False))
            == "avg(((@a))) + 3"
        )

    def test_avg_global(self, parser: ParserManager):
        assert (
            "".join(parser.replace("avg(((@a))) + @a", "@a", "3", True))
            == "avg(((3))) + 3"
        )

    def test_if(self, parser: ParserManager):
        assert (
            "".join(parser.replace("if(@a=3,'ДА', 'Нет')", "@a", "3", False))
            == "if(3=3,'ДА', 'Нет')"
        )

    def test_if_and_avg_false(self, parser: ParserManager):
        assert (
            "".join(parser.replace("if(avg(@a)=3,'ДА', 'Нет')", "@a", "[3]", False))
            == "if(avg(@a)=3,'ДА', 'Нет')"
        )

    def test_if_and_avg_true(self, parser: ParserManager):
        assert (
            "".join(parser.replace("if(avg(@a)=3,'ДА', 'Нет')", "@a", "[3]", True))
            == "if(avg([3])=3,'ДА', 'Нет')"
        )

    def test_safe_lower_v1(self, parser: ParserManager):
        text = "0.8*null is null THEN NULL end"
        assert "".join(parser.safe_lower(text)) == "0.8*null is null then null end"

    def test_safe_lower_v2(self, parser: ParserManager):
        text = "0.8 * 1 IS NULL THEN NULL WHEN 0.8 * 1 >= 120 THEN 'B120' ELSE 'не определён' END"
        assert "".join(parser.safe_lower(text)) == "0.8 * 1 is null then null when 0.8 * 1 >= 120 then 'B120' else 'не определён' end"

import pytest

from formula_commit.parser import ParserManager


@pytest.fixture
def parser():
    return ParserManager()


class TestParser:
    
    def test_avg_local(self, parser: ParserManager):
        assert "".join(parser.replace("avg(((@a))) + @a", "@a", "3", False)) == "avg(((@a))) + 3"

    def test_avg_global(self, parser: ParserManager):
        assert "".join(parser.replace("avg(((@a))) + @a", "@a", "3", True)) == "avg(((3))) + 3"

    def test_if(self, parser: ParserManager):
        assert "".join(parser.replace("if(@a=3,'ДА', 'Нет')", "@a", "3", False)) == "if(3=3,'ДА', 'Нет')"

    def test_if_and_avg_false(self, parser):
        assert "".join(parser.replace("if(avg(@a)=3,'ДА', 'Нет')", "@a", "[3]", False)) == "if(avg(@a)=3,'ДА', 'Нет')"

    def test_if_and_avg_true(self, parser):
        assert "".join(parser.replace("if(avg(@a)=3,'ДА', 'Нет')", "@a", "[3]", True)) == "if(avg([3])=3,'ДА', 'Нет')"

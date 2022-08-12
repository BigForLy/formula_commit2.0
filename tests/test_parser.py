import pytest

from parser import ParserManager


@pytest.fixture
def parser():
    return ParserManager()


class TestParser:
    
    def test_avg_local(self, parser: ParserManager):
        assert "".join(parser.replace("avg(((@a))) + @a", "@a", "3", False)) == "avg(((@a))) + 3"

    def test_avg_global(self, parser: ParserManager):
        assert "".join(parser.replace("avg(((@a))) + @a", "@a", "3", True)) == "avg(((3))) + 3"

    def test_if(self, parser):
        pass

    def test_if_and_avg(self, parser):
        pass

class Null:
    """
    Результат выполнения формул или пустых элементов
    """

    def __add__(self, other):
        return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __rsub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __rtruediv__(self, other):
        return self

    def __iter__(self):
        return []

    def __next__(self):
        raise StopIteration

    def __bool__(self):
        return False

    def __eq__(self, other):
        "=="
        return False

    def __ne__(self, other):
        "!="
        return False

    def __lt__(self, other):
        "<"
        return float("nan") < other

    def __gt__(self, other):
        ">"
        return float("nan") > other

    def __le__(self, other):
        "<="
        return float("nan") <= other

    def __ge__(self, other):
        ">="
        return float("nan") >= other

    def __repr__(self) -> str:
        return "null"

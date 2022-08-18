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

    def __repr__(self) -> str:
        return f"null"

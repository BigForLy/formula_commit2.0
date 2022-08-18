from __future__ import annotations
from decimal import Decimal
from typing import Any, Tuple


class MDecimal(Decimal):
    def __add__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__add__(MDecimal(str(other))))
        return MDecimal(super().__add__(other))

    def __radd__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__radd__(MDecimal(str(other))))
        return MDecimal(super().__radd__(other))

    def __sub__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__sub__(MDecimal(str(other))))
        return MDecimal(super().__sub__(other))

    def __rsub__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__rsub__(MDecimal(str(other))))
        return MDecimal(super().__rsub__(other))

    def __mul__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__mul__(MDecimal(str(other))))
        return MDecimal(super().__mul__(other))

    def __rmul__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__rmul__(MDecimal(str(other))))
        return MDecimal(super().__rmul__(other))

    def __truediv__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__truediv__(MDecimal(str(other))))
        return MDecimal(super().__truediv__(other))

    def __rtruediv__(self, other) -> MDecimal:
        if isinstance(other, float):
            return MDecimal(super().__rtruediv__(MDecimal(str(other))))
        return MDecimal(super().__rtruediv__(other))

    def __round__(self, n):
        return MDecimal(super().__round__(n))

    def __pow__(self, *args: Tuple[Any]) -> MDecimal:
        return MDecimal(super().__pow__(*args))

    def quantize(self, *args: Tuple[Any]) -> MDecimal:
        return MDecimal(super().quantize(*args))

    def __repr__(self) -> str:
        return f"M{super().__repr__()}"

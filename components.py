from abc import ABC, abstractmethod
from fields import BaseField


class Component(ABC):
    @abstractmethod
    def accept(self, visitor) -> None:
        pass


class ConcreteComponentRoundTo(Component):
    """
    округление
    """

    def accept(self, visitor: BaseField) -> None:
        visitor.value = round(visitor.value, abs(visitor.round_to))

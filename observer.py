from __future__ import annotations
from typing import List, Protocol
from contextlib import suppress


class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, modifier: Observer | None = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

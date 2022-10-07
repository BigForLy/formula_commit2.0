from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Protocol
from contextlib import suppress


class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: Dict[str, List[Observer]] = defaultdict(list)

    def attach(self, observer: Observer, symbol: str):
        """
        подписывает поле observer на символьное обозначение symbol другого поля
        """
        if observer not in self._observers[symbol]:
            self._observers[symbol].append(observer)

    def detach(self, observer: Observer):
        for key, _ in self._observers.items():
            with suppress(ValueError):
                self._observers[key].remove(observer)

    def notify(self, symbol: str) -> None:
        for observer in self._observers[symbol]:
            observer.update(self)

    def pop_observers(self):
        for _, values in self._observers.items():
            if values:
                yield from values
        self._observers.clear()

    @property
    def is_observers_empty(self) -> bool:
        for _, value in self._observers.items():
            if value:
                break
        else:
            return True
        return False

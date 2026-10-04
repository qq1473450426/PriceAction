from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Signal:
    side: str
    score: float
    confidence: float
    price: float
    reason: str


class BaseStrategy(ABC):
    name = "base"

    @abstractmethod
    def evaluate(self, snapshot):
        raise NotImplementedError

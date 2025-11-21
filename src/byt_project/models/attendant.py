from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .employee import Employee


@dataclass
class Attendant(Employee):
    MODEL_TYPE: ClassVar[str] = "attendant"

    languages: list[str]
    is_training_completed: bool

    def __post_init__(self) -> None:
        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")

    def get_assigned_flights(self) -> list[str]:
        raise NotImplementedError

    def report(self, message: str) -> None:
        raise NotImplementedError
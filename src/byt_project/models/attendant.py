from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping, Any, Self

from .employee import Employee


@dataclass
class Attendant(Employee):
    MODEL_TYPE: ClassVar[str] = "attendant"

    languages: list[str]
    is_training_completed: bool

    def __post_init__(self) -> None:
        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        base = Employee.from_dict(data)
        return cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            languages=list(data["languages"]),
            is_training_completed=bool(data["is_training_completed"]),
        )

    def get_assigned_flights(self) -> list[str]:
        raise NotImplementedError

    def report(self, message: str) -> None:
        raise NotImplementedError
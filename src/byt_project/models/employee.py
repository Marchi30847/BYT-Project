from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import ClassVar, Any, cast

from .base import BaseModel


class Shift(Enum):
    DAY = "day"
    NIGHT = "night"


@dataclass(kw_only=True)
class Employee(BaseModel):
    MODEL_TYPE: ClassVar[str] = "employee"

    hire_date: date
    salary: float
    shift: Shift


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data["hire_date"] = self.hire_date.isoformat()
        data["shift"] = self.shift.value

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Employee:
        data_copy: dict[str, Any] = dict(data)

        raw_date: Any = data_copy.get("hire_date")
        if isinstance(raw_date, str):
            data_copy["hire_date"] = date.fromisoformat(raw_date)

        raw_shift: Any = data_copy.get("shift")
        if raw_shift in {s.value for s in Shift}:
            data_copy["shift"] = Shift(raw_shift)
        else:
            # todo validate
            data_copy["shift"] = None

        instance = cast(Employee, super().from_dict(data_copy))

        return instance

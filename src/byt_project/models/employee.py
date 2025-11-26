from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Mapping, Any, Self, ClassVar

from src.byt_project.models.airline import Airline
from src.byt_project.models.base import BaseModel


class Shift(Enum):
    DAY = "day"
    NIGHT = "night"


@dataclass
class Employee(BaseModel):
    MODEL_TYPE: ClassVar[str] = "employee"

    hire_date: date
    salary: float
    shift: Shift
    airline: Airline | None = None

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        kwargs = dict(data)
        kwargs.pop("type", None)
        id_ = kwargs.pop("id", None)

        hire_date = date.fromisoformat(kwargs["hire_date"])
        salary = float(kwargs["salary"])
        shift = Shift(kwargs["shift"])

        obj = cls(
            hire_date=hire_date,
            salary=salary,
            shift=shift,
        )
        obj.id = id_
        return obj

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["hire_date"] = self.hire_date.isoformat()
        d["shift"] = self.shift.value
        return d
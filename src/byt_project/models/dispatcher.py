from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping, Any, Self

from .employee import Employee


@dataclass
class Dispatcher(Employee):
    MODEL_TYPE: ClassVar[str] = "dispatcher"

    specialization: str
    certification_level: int

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        base = Employee.from_dict(data)
        return cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            specialization=str(data["specialization"]),
            certification_level=int(data["certification_level"]),
        )
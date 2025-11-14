from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping, Any, Self

from .employee import Employee


@dataclass
class SecurityOfficer(Employee):
    MODEL_TYPE: ClassVar[str] = "security_officer"

    assigned_zone: str
    is_armed: bool
    on_duty: bool
    supervisor_id: int | None = None

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        base = Employee.from_dict(data)
        return cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            assigned_zone=str(data["assigned_zone"]),
            is_armed=bool(data["is_armed"]),
            on_duty=bool(data["on_duty"]),
            supervisor_id=(
                int(data["supervisor_id"]) if data.get("supervisor_id") is not None else None
            ),
        )
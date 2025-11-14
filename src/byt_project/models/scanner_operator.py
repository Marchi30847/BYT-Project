from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping, Any, Self

from .employee import Employee
from .security_officer import SecurityOfficer


@dataclass
class ScannerOperator(Employee):
    MODEL_TYPE: ClassVar[str] = "scanner_operator"

    authorized_scanner_types: list[str]
    incidents_reported: int = 0

    def __post_init__(self) -> None:
        if not (1 <= len(self.authorized_scanner_types) <= 2):
            raise ValueError("ScannerOperator must have 1 or 2 authorized scanner types")

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        base = SecurityOfficer.from_dict(data)
        return cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            assigned_zone=base.assigned_zone,
            is_armed=base.is_armed,
            on_duty=base.on_duty,
            supervisor_id=base.supervisor_id,
            authorized_scanner_types=list(data["authorized_scanner_types"]),
            incidents_reported=int(data["incidents_reported"]),
        )

    def report_incident(self, description: str) -> None:
        raise NotImplementedError
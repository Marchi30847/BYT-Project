from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .employee import Employee


@dataclass
class SecurityOfficer(Employee):
    MODEL_TYPE: ClassVar[str] = "security_officer"

    assigned_zone: str
    is_armed: bool
    on_duty: bool
    supervisor_id: int | None = None
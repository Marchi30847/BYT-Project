from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from . import BaseModel
from .employee import Employee
from .terminal import Terminal


@dataclass
class SecurityOfficer(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "security_officer"

    assigned_zone: str
    is_armed: bool
    on_duty: bool
    terminal: Terminal
    manager: SecurityOfficer | None = None
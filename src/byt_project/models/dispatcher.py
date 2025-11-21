from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .employee import Employee


@dataclass
class Dispatcher(Employee):
    MODEL_TYPE: ClassVar[str] = "dispatcher"

    specialization: str
    certification_level: int
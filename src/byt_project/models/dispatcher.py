from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from . import BaseModel
from .employee import Employee
from .flight import Flight
from .terminal import Terminal


@dataclass
class Dispatcher(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "dispatcher"

    specialization: str
    certification_level: int

    terminal: Terminal
    flights: list[Flight] | None = None

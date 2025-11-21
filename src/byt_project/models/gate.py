from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Optional, List

from .base import BaseModel
from .terminal import Terminal


@dataclass
class Gate(BaseModel):
    MODEL_TYPE: ClassVar[str] = "gate"

    number: int
    terminal: Optional[Terminal] = None
    is_open: bool = True
    flights: List = field(default_factory=list)

    def add_flight(self, flight):
        if not self.is_open:
            raise ValueError(f"Gate {self.number} is closed. Cannot assign flight.")

        flight.gate = self
        self.flights.append(flight)

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False
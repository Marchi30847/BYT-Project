from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, List

from .base import BaseModel
from .flight import Flight
from .terminal import Terminal


@dataclass(kw_only=True)
class Gate(BaseModel):
    MODEL_TYPE: ClassVar[str] = "gate"

    number: int
    terminal: Terminal | None = None
    is_open: bool = True
    flights: List[Flight] = field(default_factory=list)

    def add_flight(self, flight):
        if not self.is_open:
            raise ValueError(f"Gate {self.number} is closed. Cannot assign flight.")

        flight.gate = self
        self.flights.append(flight)

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False
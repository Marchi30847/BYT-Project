from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from . import BaseModel
from .employee import Employee
from .flight import Flight, FlightStatus


@dataclass
class Attendant(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "attendant"

    languages: list[str]
    is_training_completed: bool
    flights: list[Flight] | None = None


    def __post_init__(self) -> None:
        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")

    def get_assigned_flights(self):
        return (f for f in self.flights if f.status == FlightStatus.SCHEDULED)

    def report(self, message: str) -> None:
        raise NotImplementedError
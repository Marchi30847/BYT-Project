from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING

from . import AirlineStaff

if TYPE_CHECKING:
    from .flight import Flight, FlightStatus


@dataclass(kw_only=True)
class Attendant(AirlineStaff):
    MODEL_TYPE: ClassVar[str] = "attendant"

    is_training_completed: bool
    languages: list[str] = field(default_factory=list)

    flights: list[Flight] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")


    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data.pop("flights", None)

        return data

    def get_assigned_flights(self) -> list[Flight]:
        return [f for f in self.flights if f.status == FlightStatus.SCHEDULED]

    def report(self, message: str) -> None:
        print(f"Attendant {self.id} reports: {message}")

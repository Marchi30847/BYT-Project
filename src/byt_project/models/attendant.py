from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import ClassVar, Any, TYPE_CHECKING

from .employee import Employee

if TYPE_CHECKING:
    from .flight import Flight, FlightStatus


@dataclass(kw_only=True)
class Attendant(Employee):
    MODEL_TYPE: ClassVar[str] = "attendant"

    languages: list[str] = field(default_factory=list)
    is_training_completed: bool = False

    flights: list[Flight] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data.pop("flights", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Attendant:
        valid_arg_names = {f.name for f in fields(cls) if f.init}
        clean_kwargs = {k: v for k, v in data.items() if k in valid_arg_names}

        instance = cls(**clean_kwargs)

        raw_id: str | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        raw_airline_id: str | None = data.get("airline_id")
        instance.airline_id = int(raw_airline_id) if raw_airline_id is not None else None

        return instance

    def get_assigned_flights(self) -> list[Flight]:
        from .flight import FlightStatus
        return [f for f in self.flights if f.status == FlightStatus.SCHEDULED]

    def report(self, message: str) -> None:
        print(f"Attendant {self.id} reports: {message}")

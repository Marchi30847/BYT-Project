from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .airline_staff import AirlineStaff

if TYPE_CHECKING:
    from .flight import Flight, FlightStatus


@dataclass(kw_only=True)
class Attendant(AirlineStaff):
    MODEL_TYPE: ClassVar[str] = "attendant"

    is_training_completed: bool
    languages: list[str] = field(default_factory=list)

    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    @property
    def flights(self) -> list[Flight]:
        if self._flights is not None:
            return self._flights

        if self.id is not None:
            loaded: list[Flight] | None = self._run_loader("flights", self.id)
            if loaded is not None:
                self._flights = loaded
                return self._flights

        self._flights = []
        return self._flights

    @flights.setter
    def flights(self, value: list[Flight]) -> None:
        self._flights = value


    def __post_init__(self) -> None:
        super().__post_init__()

        # is_training_completed
        if not isinstance(self.is_training_completed, bool):
            raise TypeError("is_training_completed must be a boolean")

        # languages
        if not isinstance(self.languages, list):
            raise TypeError("languages must be a list")

        if len(self.languages) < 2:
            raise ValueError("Attendant must know at least two languages")

        for lang in self.languages:
            if not isinstance(lang, str) or not lang.strip():
                raise ValueError("All languages must be non-empty strings")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Attendant:
        instance = cast(Attendant, super().from_dict(data))

        cls._restore_many_fk(instance, data, "flight_ids", "flight_ids")

        return instance

    def get_assigned_flights(self) -> list[Flight]:
        return [f for f in self.flights if f.status == FlightStatus.SCHEDULED]

    def report(self, message: str) -> None:
        print(f"Attendant {self.id} reports: {message}")

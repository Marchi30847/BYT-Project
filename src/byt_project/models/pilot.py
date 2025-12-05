from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .airline_staff import AirlineStaff

if TYPE_CHECKING:
    from .flight import Flight


class PilotRank(Enum):
    CAPTAIN = "captain"
    FIRST_OFFICER = "first_officer"


@dataclass(kw_only=True)
class Pilot(AirlineStaff):
    MODEL_TYPE: ClassVar[str] = "pilot"

    licence_number: str
    rank: PilotRank
    flight_hours: int

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

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data["rank"] = self.rank.value

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Pilot:
        data_copy: dict[str, Any] = dict(data)

        raw_rank: Any = data_copy.get("rank")
        if raw_rank in {r.value for r in PilotRank}:
            data_copy["rank"] = PilotRank(raw_rank)
        else:
            # todo validate
            data_copy["rank"] = None

        instance = cast(Pilot, super().from_dict(data_copy))

        return instance

    def get_assigned_flights(self) -> list[Flight]:
        from .flight import FlightStatus
        return [f for f in self.flights if f.status == FlightStatus.SCHEDULED]

    def report(self, message: str) -> None:
        print(f"Pilot {self.licence_number} ({self.rank.value}) reports: {message}")

    def request_landing(self, airport_code: str) -> None:
        print(f"Pilot {self.id} requesting landing at {airport_code}")

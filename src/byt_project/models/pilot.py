from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Mapping, Any, Self, Generator

from . import BaseModel
from .employee import Employee
from .flight import FlightStatus, Flight


class PilotRank(Enum):
    CAPTAIN = "captain"
    FIRST_OFFICER = "first_officer"


@dataclass
class Pilot(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "pilot"

    licence_number: str
    rank: PilotRank
    flight_hours: int
    flights: list[Flight] | None = None

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        kwargs = dict(data)
        kwargs.pop("type", None)
        id_ = kwargs.pop("id", None)

        base = Employee.from_dict(kwargs)

        obj = cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            licence_number=str(kwargs["licence_number"]),
            rank=PilotRank(kwargs["rank"]),
            flight_hours=int(kwargs["flight_hours"]),
        )
        obj.id = id_
        return obj

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["rank"] = self.rank.value
        return d

    def get_assigned_flights(self):
        return (f for f in self.flights if f.status == FlightStatus.SCHEDULED)

    def report(self, message: str) -> None:
        raise NotImplementedError

    def request_landing(self, airport_code: str) -> None:
        raise NotImplementedError
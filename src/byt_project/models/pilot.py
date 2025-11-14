from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Mapping, Any, Self

from .employee import Employee


class PilotRank(Enum):
    CAPTAIN = "captain"
    FIRST_OFFICER = "first_officer"


@dataclass
class Pilot(Employee):
    MODEL_TYPE: ClassVar[str] = "pilot"

    licence_number: str
    rank: PilotRank
    flight_hours: int

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        base = Employee.from_dict(data)
        return cls(
            hire_date=base.hire_date,
            salary=base.salary,
            shift=base.shift,
            licence_number=str(data["licence_number"]),
            rank=PilotRank(data["rank"]),
            flight_hours=int(data["flight_hours"]),
        )

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["rank"] = self.rank.value
        return d

    def get_assigned_flights(self) -> list[str]:
        raise NotImplementedError

    def report(self, message: str) -> None:
        raise NotImplementedError

    def request_landing(self, airport_code: str) -> None:
        raise NotImplementedError
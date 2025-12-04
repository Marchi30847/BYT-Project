from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .employee import Employee

if TYPE_CHECKING:
    from .airline import Airline


@dataclass(kw_only=True)
class AirlineStaff(Employee):
    MODEL_TYPE: ClassVar[str] = "airline_staff"

    airline_id: int | None = field(default=None, init=False)
    airline: Airline | None = field(default=None)

    def __post_init__(self) -> None:
        if self.airline and getattr(self.airline, 'id', None) is not None:
            self.airline_id = self.airline.id

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.airline:
            data["airline_id"] = self.airline.id
        elif self.airline_id is not None:
            data["airline_id"] = self.airline_id
        else:
            data["airline_id"] = None

        data.pop("airline", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AirlineStaff:
        instance = cast(AirlineStaff, super().from_dict(data))

        raw_airline_id: str | int | None = data.get("airline_id")
        instance.airline_id = int(raw_airline_id) if raw_airline_id is not None else None

        return instance

from __future__ import annotations

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import ClassVar, Any, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .airline import Airline
    from .flight import Flight


@dataclass(kw_only=True)
class Airplane(BaseModel):
    MODEL_TYPE: ClassVar[str] = "airplane"

    model: str
    manufacturer: str
    capacity: int
    max_luggage_weight: float
    year_of_manufacture: int

    airline_id: int | None = field(default=None, init=False)
    airline: Airline | None = field(default=None)

    flights: list[Flight] = field(default_factory=list)

    max_service_years: ClassVar[int] = 30

    def __post_init__(self) -> None:
        if self.airline and getattr(self.airline, 'id', None) is not None:
            self.airline_id = self.airline.id

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.airline:
            data["airline_id"] = self.airline.id
        else:
            data["airline_id"] = None

        data.pop("flights", None)
        data.pop("airline", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Airplane:
        valid_arg_names: set[str] = {f.name for f in fields(cls) if f.init}
        clean_kwargs: dict[str, Any] = {k: v for k, v in data.items() if k in valid_arg_names}

        instance = cls(**clean_kwargs)

        raw_airline_id: str | int | None = data.get("airline_id")
        instance.airline_id = int(raw_airline_id) if raw_airline_id is not None else None

        raw_id: str | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        return instance


    def years_in_service(self) -> int:
        return datetime.now().year - self.year_of_manufacture

    def is_expired(self) -> bool:
        return self.years_in_service() > self.max_service_years

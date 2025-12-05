from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Any, TYPE_CHECKING, cast

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
    _airline: Airline | None = field(default=None, init=False, repr=False)

    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    max_service_years: ClassVar[int] = 30

    @property
    def airline(self) -> Airline | None:
        if self._airline is not None:
            return self._airline

        if self.airline_id is None:
            return None

        loaded: Airline | None = self._run_loader("airline", self.airline_id)
        if loaded:
            self._airline = loaded

        return self._airline

    @airline.setter
    def airline(self, value: Airline | None) -> None:
        self._airline = value
        if value and getattr(value, 'id', None) is not None:
            self.airline_id = value.id
        else:
            self.airline_id = None

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
        data: dict[str, Any] = super().to_dict()

        data["airline_id"] = self._get_fk_value(self._airline, self.airline_id)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Airplane:
        instance = cast(Airplane, super().from_dict(data))

        cls._restore_fk(instance, data, "airline_id", "airline_id")

        return instance

    def years_in_service(self) -> int:
        return datetime.now().year - self.year_of_manufacture

    def is_expired(self) -> bool:
        return self.years_in_service() > self.max_service_years

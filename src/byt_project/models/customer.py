from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .person import Person

if TYPE_CHECKING:
    from .flight import Flight


@dataclass(kw_only=True)
class Customer(Person):
    MODEL_TYPE: ClassVar[str] = "customer"

    email: str
    phone_number: str

    flight_ids: list[int] = field(default_factory=list, init=False)
    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    @property
    def flights(self) -> list[Flight]:
        if self._flights is not None:
            return self._flights

        if self.flight_ids:
            loaded: list[Flight] | None = self._run_loader("flights", self.flight_ids)
            if loaded is not None:
                self._flights = loaded
                return self._flights

        self._flights = []
        return self._flights

    @flights.setter
    def flights(self, value: list[Flight]) -> None:
        self._flights = value
        self.flight_ids = [f.id for f in value if f.id is not None]


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["flight_ids"] = self._get_many_fk_value(self._flights, self.flight_ids)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Customer:
        instance = cast(Customer, super().from_dict(data))

        cls._restore_many_fk(instance, data, "flight_ids", "flight_ids")

        return instance


    def self_check_in(self) -> None:
        print(f"Customer {self.name} {self.surname} is checking in...")

    def book_flight(self, flight: Flight) -> None:
        self.flights.append(flight)
        if flight.id is not None:
            self.flight_ids.append(flight.id)

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar, Any, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .attendant import Attendant
    from .airplane import Airplane
    from .destination import Destination
    from .dispatcher import Dispatcher
    from .gate import Gate
    from .pilot import Pilot
    from .route import Route


class FlightStatus(Enum):
    SCHEDULED = "Scheduled"
    BOARDING = "Boarding"
    DEPARTED = "Departed"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"


@dataclass(kw_only=True)
class Flight(BaseModel):
    MODEL_TYPE: ClassVar[str] = "flight"

    flight_number: str
    departure_time: datetime
    arrival_time: datetime | None = None
    status: FlightStatus = FlightStatus.SCHEDULED

    available_seats: int = field(init=False, default=0)


    gate: Gate | None = None
    gate_id: int | None = field(default=None, init=False)

    captain: Pilot | None = None
    captain_id: int | None = field(default=None, init=False)

    route: Route | None = None
    route_id: int | None = field(default=None, init=False)

    airplane: Airplane | None = None
    airplane_id: int | None = field(default=None, init=False)

    dispatcher: Dispatcher | None = None
    dispatcher_id: int | None = field(default=None, init=False)

    destination: Destination | None = None
    destination_id: int | None = field(default=None, init=False)


    pilots: list[Pilot] = field(default_factory=list)
    attendants: list[Attendant] = field(default_factory=list)

    def __post_init__(self):
        if self.gate and getattr(self.gate, 'id', None): self.gate_id = self.gate.id
        if self.captain and getattr(self.captain, 'id', None): self.capitan_id = self.captain.id
        if self.route and getattr(self.route, 'id', None): self.route_id = self.route.id
        if self.airplane and getattr(self.airplane, 'id', None): self.airplane_id = self.airplane.id
        if self.dispatcher and getattr(self.dispatcher, 'id', None): self.dispatcher_id = self.dispatcher.id
        if self.destination and getattr(self.destination, 'id', None): self.destination_id = self.destination.id

        if self.airplane:
            self.available_seats = self.airplane.capacity
        else:
            self.available_seats = 0

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["departure_time"] = self.departure_time.isoformat()
        if self.arrival_time:
            data["arrival_time"] = self.arrival_time.isoformat()

        data["status"] = self.status.value

        def set_id(obj_field, id_field, key_name):
            if obj_field:
                data[key_name] = obj_field.id
            elif id_field is not None:
                data[key_name] = id_field
            else:
                data[key_name] = None

        set_id(self.gate, self.gate_id, "gate_id")
        set_id(self.captain, self.capitan_id, "capitan_id")
        set_id(self.route, self.route_id, "route_id")
        set_id(self.airplane, self.airplane_id, "airplane_id")
        set_id(self.dispatcher, self.dispatcher_id, "dispatcher_id")
        set_id(self.destination, self.destination_id, "destination_id")

        data["pilot_ids"] = [p.id for p in self.pilots if p.id is not None]
        data["attendant_ids"] = [a.id for a in self.attendants if a.id is not None]

        data.pop("gate", None)
        data.pop("capitan", None)
        data.pop("route", None)
        data.pop("airplane", None)
        data.pop("dispatcher", None)
        data.pop("destination", None)
        data.pop("pilots", None)
        data.pop("attendants", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Flight:
        kwargs: dict[str, Any] = dict(data)
        kwargs.pop("type", None)

        kwargs["departure_time"] = datetime.fromisoformat(kwargs["departure_time"])
        if kwargs.get("arrival_time"):
            kwargs["arrival_time"] = datetime.fromisoformat(kwargs["arrival_time"])

        if kwargs.get("status"):
            kwargs["status"] = FlightStatus(kwargs["status"])

        gate_id: str | None = kwargs.pop("gate_id", None)
        capitan_id: str | None = kwargs.pop("capitan_id", None)
        route_id: str | None = kwargs.pop("route_id", None)
        airplane_id: str | None = kwargs.pop("airplane_id", None)
        dispatcher_id: str | None = kwargs.pop("dispatcher_id", None)
        destination_id: str | None = kwargs.pop("destination_id", None)

        # handle
        kwargs.pop("pilot_ids", None)
        kwargs.pop("attendant_ids", None)

        kwargs.pop("gate", None)
        kwargs.pop("capitan", None)
        kwargs.pop("route", None)
        kwargs.pop("airplane", None)
        kwargs.pop("dispatcher", None)
        kwargs.pop("destination", None)
        kwargs.pop("pilots", None)
        kwargs.pop("attendants", None)

        obj = cls(**kwargs)

        obj.gate_id = int(gate_id) if gate_id is not None else None
        obj.capitan_id = int(capitan_id) if capitan_id is not None else None
        obj.route_id = int(route_id) if route_id is not None else None
        obj.airplane_id = int(airplane_id) if airplane_id is not None else None
        obj.dispatcher_id = int(dispatcher_id) if dispatcher_id is not None else None
        obj.destination_id = int(destination_id) if destination_id is not None else None

        return obj


    def cancel(self):
        self.status = FlightStatus.CANCELLED

    def assign_pilot(self, pilot: Pilot):
        if len(self.pilots) < 2:
            self.pilots.append(pilot)
        else:
            raise ValueError("Flight already has two pilots")

    def assign_attendant(self, attendant: Attendant):
        self.attendants.append(attendant)

    def book_seat(self, count: int = 1) -> bool:
        if self.available_seats >= count:
            self.available_seats -= count
            return True

        return False

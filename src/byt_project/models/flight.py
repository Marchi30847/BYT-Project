from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar, Any, TYPE_CHECKING, cast

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


    gate_id: int | None = field(default=None, init=False)
    gate: Gate | None = field(default=None)

    captain_id: int | None = field(default=None, init=False)
    captain: Pilot | None = field(default=None)

    route_id: int | None = field(default=None, init=False)
    route: Route | None = field(default=None)

    airplane_id: int | None = field(default=None, init=False)
    airplane: Airplane | None = field(default=None)

    dispatcher_id: int | None = field(default=None, init=False)
    dispatcher: Dispatcher | None = field(default=None)

    destination_id: int | None = field(default=None, init=False)
    destination: Destination | None = field(default=None)


    pilot_ids: list[int] = field(default_factory=list, init=False)
    pilots: list[Pilot] = field(default_factory=list)

    attendant_ids: list[int] = field(default_factory=list, init=False)
    attendants: list[Attendant] = field(default_factory=list)


    def __post_init__(self) -> None:
        if self.gate and getattr(self.gate, 'id', None): self.gate_id = self.gate.id
        if self.captain and getattr(self.captain, 'id', None): self.captain_id = self.captain.id
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


        def save_fk(obj_field, id_field, key):
            if obj_field:
                data[key] = obj_field.id
            elif id_field is not None:
                data[key] = id_field
            else:
                data[key] = None

        save_fk(self.gate, self.gate_id, "gate_id")
        save_fk(self.captain, self.captain_id, "captain_id")
        save_fk(self.route, self.route_id, "route_id")
        save_fk(self.airplane, self.airplane_id, "airplane_id")
        save_fk(self.dispatcher, self.dispatcher_id, "dispatcher_id")
        save_fk(self.destination, self.destination_id, "destination_id")


        p_ids: list[int] = [p.id for p in self.pilots if p.id is not None]
        if not p_ids and self.pilot_ids:
            p_ids = self.pilot_ids
        data["pilot_ids"] = p_ids

        a_ids: list[int] = [a.id for a in self.attendants if a.id is not None]
        if not a_ids and self.attendant_ids:
            a_ids = self.attendant_ids
        data["attendant_ids"] = a_ids

        for k in ["gate", "captain", "route", "airplane", "dispatcher", "destination", "pilots", "attendants"]:
            data.pop(k, None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Flight:
        data_copy: dict[str, Any] = dict(data)

        raw_dep: Any = data_copy.get("departure_time")
        if isinstance(raw_dep, str):
            data_copy["departure_time"] = datetime.fromisoformat(raw_dep)

        raw_arr: Any = data_copy.get("arrival_time")
        if isinstance(raw_arr, str):
            data_copy["arrival_time"] = datetime.fromisoformat(raw_arr)

        raw_status: Any = data_copy.get("status")
        if raw_status in {s.value for s in FlightStatus}:
            data_copy["status"] = FlightStatus(raw_status)
        else:
            data_copy["status"] = None

        instance = cast(Flight, super().from_dict(data_copy))


        def restore_fk(key, attr_name):
            raw_val: str | int | None = data_copy.get(key)
            setattr(instance, attr_name, int(raw_val) if raw_val is not None else None)
            if raw_val is not None:
                setattr(instance, attr_name, int(raw_val))

        restore_fk("gate_id", "gate_id")
        restore_fk("captain_id", "captain_id")
        restore_fk("route_id", "route_id")
        restore_fk("airplane_id", "airplane_id")
        restore_fk("dispatcher_id", "dispatcher_id")
        restore_fk("destination_id", "destination_id")

        raw_pilot_ids: list[Any] = data.get("pilot_ids")
        if isinstance(raw_pilot_ids, list):
            instance.pilot_ids = [int(x) for x in raw_pilot_ids]

        raw_attendant_ids: list[Any] = data.get("attendant_ids")
        if isinstance(raw_attendant_ids, list):
            instance.attendant_ids = [int(x) for x in raw_attendant_ids]

        return instance

    def cancel(self) -> None:
        self.status = FlightStatus.CANCELLED

    def assign_pilot(self, pilot: Pilot) -> None:
        if len(self.pilots) < 2:
            self.pilots.append(pilot)
        else:
            raise ValueError("Flight already has two pilots")

    def assign_attendant(self, attendant: Attendant) -> None:
        self.attendants.append(attendant)

    def book_seat(self, count: int = 1) -> bool:
        if self.available_seats >= count:
            self.available_seats -= count

            return True

        return False

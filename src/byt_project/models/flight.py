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
    from .customer import Customer


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
    _gate: Gate | None = field(default=None, init=False, repr=False)

    @property
    def gate(self) -> Gate | None:
        if self._gate is not None:
            return self._gate

        if self.gate_id is None:
            return None

        loaded: Gate | None = self._run_loader("gate", self.gate_id)
        if loaded:
            self._gate = loaded

        return self._gate

    @gate.setter
    def gate(self, value: Gate | None) -> None:
        self._gate = value
        if value and getattr(value, 'id', None) is not None:
            self.gate_id = value.id
        else:
            self.gate_id = None

    captain_id: int | None = field(default=None, init=False)
    _captain: Pilot | None = field(default=None, init=False, repr=False)

    @property
    def captain(self) -> Pilot | None:
        if self._captain is not None:
            return self._captain

        if self.captain_id is None:
            return None

        loaded: Pilot | None = self._run_loader("captain", self.captain_id)
        if loaded:
            self._captain = loaded

        return self._captain

    @captain.setter
    def captain(self, value: Pilot | None) -> None:
        self._captain = value
        if value and getattr(value, 'id', None) is not None:
            self.captain_id = value.id
        else:
            self.captain_id = None

    route_id: int | None = field(default=None, init=False)
    _route: Route | None = field(default=None, init=False, repr=False)

    @property
    def route(self) -> Route | None:
        if self._route is not None:
            return self._route

        if self.route_id is None:
            return None

        loaded: Route | None = self._run_loader("route", self.route_id)
        if loaded:
            self._route = loaded

        return self._route

    @route.setter
    def route(self, value: Route | None) -> None:
        self._route = value
        if value and getattr(value, 'id', None) is not None:
            self.route_id = value.id
        else:
            self.route_id = None

    airplane_id: int | None = field(default=None, init=False)
    _airplane: Airplane | None = field(default=None, init=False, repr=False)

    @property
    def airplane(self) -> Airplane | None:
        if self._airplane is not None:
            return self._airplane

        if self.airplane_id is None:
            return None

        loaded: Airplane | None = self._run_loader("airplane", self.airplane_id)
        if loaded:
            self._airplane = loaded

        return self._airplane

    @airplane.setter
    def airplane(self, value: Airplane | None) -> None:
        self._airplane = value
        if value and getattr(value, 'id', None) is not None:
            self.airplane_id = value.id
        else:
            self.airplane_id = None

    dispatcher_id: int | None = field(default=None, init=False)
    _dispatcher: Dispatcher | None = field(default=None, init=False, repr=False)

    @property
    def dispatcher(self) -> Dispatcher | None:
        if self._dispatcher is not None:
            return self._dispatcher

        if self.dispatcher_id is None:
            return None

        loaded: Dispatcher | None = self._run_loader("dispatcher", self.dispatcher_id)
        if loaded:
            self._dispatcher = loaded

        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, value: Dispatcher | None) -> None:
        self._dispatcher = value
        if value and getattr(value, 'id', None) is not None:
            self.dispatcher_id = value.id
        else:
            self.dispatcher_id = None

    destination_id: int | None = field(default=None, init=False)
    _destination: Destination | None = field(default=None, init=False, repr=False)

    @property
    def destination(self) -> Destination | None:
        if self._destination is not None:
            return self._destination

        if self.destination_id is None:
            return None

        loaded: Destination | None = self._run_loader("destination", self.destination_id)
        if loaded:
            self._destination = loaded

        return self._destination

    @destination.setter
    def destination(self, value: Destination | None) -> None:
        self._destination = value
        if value and getattr(value, 'id', None) is not None:
            self.destination_id = value.id
        else:
            self.destination_id = None

    pilot_ids: list[int] = field(default_factory=list, init=False)
    _pilots: list[Pilot] | None = field(default=None, init=False, repr=False)

    @property
    def pilots(self) -> list[Pilot]:
        if self._pilots is not None:
            return self._pilots

        if self.pilot_ids:
            loaded: list[Pilot] | None = self._run_loader("pilots", self.pilot_ids)
            if loaded is not None :
                self._pilots = loaded
                return self._pilots

        self._pilots = []
        return self._pilots

    @pilots.setter
    def pilots(self, value: list[Pilot]) -> None:
        self._pilots = value
        self.pilot_ids = [p.id for p in value if p.id is not None]

    attendant_ids: list[int] = field(default_factory=list, init=False)
    _attendants: list[Attendant] | None = field(default=None, init=False, repr=False)

    @property
    def attendants(self) -> list[Attendant]:
        if self._attendants is not None:
            return self._attendants

        if self.attendant_ids:
            loaded: list[Attendant] | None = self._run_loader("attendants", self.attendant_ids)
            if loaded is not None :
                self._attendants = loaded
                return self._attendants

        self._attendants = []
        return self._attendants

    @attendants.setter
    def attendants(self, value: list[Attendant]) -> None:
        self._attendants = value
        self.attendant_ids = [a.id for a in value if a.id is not None]

    _customers: list[Customer] | None = field(default=None, init=False, repr=False)

    @property
    def customers(self) -> list[Customer]:
        if self._customers is not None: return self._customers

        if self.id is not None:
            loaded: list[Customer] | None = self._run_loader("customers", self.id)
            if loaded is not None :
                self._customers = loaded
                return self._customers

        self._customers = []
        return self._customers

    @customers.setter
    def customers(self, value: list[Customer]) -> None:
        self._customers = value


    def __post_init__(self) -> None:
        super().__post_init__()

        if self._airplane:
            self.available_seats = self._airplane.capacity
        else:
            self.available_seats = 0

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["departure_time"] = self.departure_time.isoformat()
        if self.arrival_time:
            data["arrival_time"] = self.arrival_time.isoformat()
        data["status"] = self.status.value

        data["gate_id"] = self._get_fk_value(self._gate, self.gate_id)
        data["captain_id"] = self._get_fk_value(self._captain, self.captain_id)
        data["route_id"] = self._get_fk_value(self._route, self.route_id)
        data["airplane_id"] = self._get_fk_value(self._airplane, self.airplane_id)
        data["dispatcher_id"] = self._get_fk_value(self._dispatcher, self.dispatcher_id)
        data["destination_id"] = self._get_fk_value(self._destination, self.destination_id)

        data["pilot_ids"] = self._get_many_fk_value(self._pilots, self.pilot_ids)
        data["attendant_ids"] = self._get_many_fk_value(self._attendants, self.attendant_ids)

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
            data_copy.pop("status", None)

        instance = cast(Flight, super().from_dict(data_copy))

        cls._restore_fk(instance, data, "gate_id", "gate_id")
        cls._restore_fk(instance, data, "captain_id", "captain_id")
        cls._restore_fk(instance, data, "route_id", "route_id")
        cls._restore_fk(instance, data, "airplane_id", "airplane_id")
        cls._restore_fk(instance, data, "dispatcher_id", "dispatcher_id")
        cls._restore_fk(instance, data, "destination_id", "destination_id")

        cls._restore_many_fk(instance, data, "pilot_ids", "pilot_ids")
        cls._restore_many_fk(instance, data, "attendant_ids", "attendant_ids")

        return instance

    def cancel(self) -> None:
        self.status = FlightStatus.CANCELLED

    def assign_pilot(self, pilot: Pilot) -> None:
        if len(self.pilots) < 2:
            self.pilots.append(pilot)
            if pilot.id is not None:
                self.pilot_ids.append(pilot.id)
        else:
            raise ValueError("Flight already has two pilots")

    def assign_attendant(self, attendant: Attendant) -> None:
        self.attendants.append(attendant)
        if attendant.id is not None:
            self.attendant_ids.append(attendant.id)

    def book_seat(self, count: int = 1) -> bool:
        if self.available_seats >= count:
            self.available_seats -= count
            return True
        return False

    def add_passenger(self, customer: Customer) -> None:
        if self.available_seats > 0:
            if self._customers is None: self._customers = []
            self._customers.append(customer)
            self.available_seats -= 1

            if self not in customer.flights:
                customer.flights.append(self)
        else:
            raise ValueError("No seats available")

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar, List, Optional

from .attendant import Attendant
from .base import BaseModel
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


@dataclass
class Flight(BaseModel):
    MODEL_TYPE: ClassVar[str] = "flight"

    flight_number: str
    departure_time: datetime
    route: Route
    airplane: Airplane
    dispatcher: Dispatcher
    destination: Destination
    arrival_time: datetime | None = None
    gate: Gate | None = None
    status: FlightStatus = FlightStatus.SCHEDULED
    available_seats: int = field(init=False)
    pilots: List[Pilot] = field(default_factory=list)
    attendants: List[Attendant] = field(default_factory=list)


    def __post_init__(self):
        self.available_seats = self.airplane.capacity

    def cancel(self):
        self.status = FlightStatus.CANCELLED

    def assign_pilot(self, pilot):
        if len(self.pilots) < 2:
            self.pilots.append(pilot)

    def assign_attendant(self, attendant):
        self.attendants.append(attendant)

    def assign_pilot(self, attendant):
        if len(self.attendants) < 2:
            self.attendants.append(attendant)
        else: raise ValueError("Flight already has two pilots")

    def book_seat(self, count: int = 1) -> bool:
        if self.available_seats >= count:
            self.available_seats -= count
            return True

        return False
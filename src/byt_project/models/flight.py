from enum import Enum
from datetime import datetime
from typing import List, Optional

from src.byt_project.models.airplane import Airplane
from src.byt_project.models.gate import Gate
from src.byt_project.models.route import Route


class FlightStatus(Enum):
    SCHEDULED = "Scheduled"
    BOARDING = "Boarding"
    DEPARTED = "Departed"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"


class Flight:
    def __init__(
        self,
        flight_number: str,
        departure_time: datetime,
        arrival_time: datetime,
        route: Route,
        airplane: Airplane,
        gate: Gate =None,
        status: FlightStatus = FlightStatus.SCHEDULED
    ):
        self.flightNumber: str = flight_number
        self.departureTime: datetime = departure_time
        self.arrivalTime: datetime = arrival_time
        self.status: FlightStatus = status

        self.route = route
        self.airplane = airplane
        self.gate = gate

        self.availableSeats: int = airplane.capacity

        self.pilots: List = []
        self.attendants: List = []


    @staticmethod
    def getFlightDetails(flights: List["Flight"], number: str) -> Optional["Flight"]:
        for f in flights:
            if f.flightNumber == number:
                return f
        return None

    def getGate(self):
        return self.gate

    @staticmethod
    def createFlight(flights_list: List["Flight"], flight: "Flight") -> None:
        flights_list.append(flight)

    def updateFlight(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def cancel(self):
        self.status = FlightStatus.CANCELLED

    def assignPilot(self, pilot):
        if len(self.pilots) < 2:
            self.pilots.append(pilot)

    def assignAttendant(self, attendant):
        self.attendants.append(attendant)

    def bookSeat(self, count: int = 1) -> bool:
        if self.availableSeats >= count:
            self.availableSeats -= count
            return True
        return False
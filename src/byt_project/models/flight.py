from enum import Enum
from datetime import datetime
from typing import List, Optional

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
        self.airplane = airplane    # объект Airplane
        self.gate = gate            # объект Gate (может быть None)

        # доступные места вычисляются из самолёта
        self.availableSeats: int = airplane.capacity

        # внутренние связи
        self.pilots: List = []      # список Pilot
        self.attendants: List = []  # список Attendant


    @staticmethod
    def getAllFlightsAvailable(flights: List["Flight"]) -> List["Flight"]:
        """Возвращает только рейсы со статусом SCHEDULED и с местами."""
        return [
            f for f in flights
            if f.status == FlightStatus.SCHEDULED and f.availableSeats > 0
        ]

    @staticmethod
    def getFlightDetails(flights: List["Flight"], number: str) -> Optional["Flight"]:
        """Ищет рейс по номеру."""
        for f in flights:
            if f.flightNumber == number:
                return f
        return None

    def getGate(self):
        """Возвращает gate, к которому привязан рейс."""
        return self.gate

    @staticmethod
    def createFlight(flights_list: List["Flight"], flight: "Flight") -> None:
        """Добавляет новый рейс."""
        flights_list.append(flight)

    def updateFlight(self, **kwargs):
        """Обновляет поля рейса. Например: updateFlight(status=FlightStatus.DELAYED)"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def cancel(self):
        """Отменяет рейс."""
        self.status = FlightStatus.CANCELLED

    # ---------------------------
    #   ADDITIONAL OPERATIONS
    # ---------------------------

    def assignPilot(self, pilot):
        """Назначить пилота (капитан должен быть минимум один)."""
        self.pilots.append(pilot)

    def assignAttendant(self, attendant):
        self.attendants.append(attendant)

    def bookSeat(self, count: int = 1) -> bool:
        """Покупка билета уменьшает количество мест."""
        if self.availableSeats >= count:
            self.availableSeats -= count
            return True
        return False

    def __repr__(self):
        return f"Flight({self.flightNumber}, {self.status.value}, seats={self.availableSeats})"
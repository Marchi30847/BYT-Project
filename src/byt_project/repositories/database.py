from __future__ import annotations

from . import AttendantRepository, DispatcherRepository, PilotRepository, GateRepository
from .airline_repository import AirlineRepository
from .airline_staff_repository import AirlineStaffRepository
from .airplane_repository import AirplaneRepository
from .flight_repository import FlightRepository


class Database:
    def __init__(self) -> None:
        self.airlines = AirlineRepository()
        self.airplanes = AirplaneRepository()
        self.dispatcher = DispatcherRepository()
        self.flights = FlightRepository()
        self.attendants = AttendantRepository()
        self.pilots = PilotRepository()
        self.airline_staff = AirlineStaffRepository()
        self.gates = GateRepository()

        self.gates.set_flight_repo(self.flights)

        self.dispatcher.set_flights(self.flights)

        self.airlines.set_airplane_repo(self.airplanes)
        self.airlines.set_airline_staff_repo(self.airline_staff)

        self.airplanes.set_airline_repo(self.airlines)
        self.airplanes.set_flight_repo(self.flights)

        # self.flights.set_airplane_repo(self.airplanes)

        self.attendants.set_flight_repo(self.flights)
        self.pilots.set_flight_repo(self.flights)

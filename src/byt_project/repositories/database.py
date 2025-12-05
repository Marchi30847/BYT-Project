from __future__ import annotations

from . import AttendantRepository, DispatcherRepository, PilotRepository
from .airline_repository import AirlineRepository
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

        self.dispatcher.set_flights(self.flights)

        # self.airlines.set_airplane_repo(self.airplanes)

        self.airplanes.set_airline_repo(self.airlines)
        self.airplanes.set_flight_repo(self.flights)

        # self.flights.set_airplane_repo(self.airplanes)

        self.attendants.set_flight_repo(self.flights)
        self.pilots.set_flight_repo(self.flights)

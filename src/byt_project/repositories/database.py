from __future__ import annotations

from . import RouteRepository, DestinationRepository
from .attendant_repository import AttendantRepository
from .dispatcher_repository import DispatcherRepository
from .pilot_repository import PilotRepository
from .gate_repository import GateRepository
from .airline_repository import AirlineRepository
from .airline_staff_repository import AirlineStaffRepository
from .airplane_repository import AirplaneRepository
from .flight_repository import FlightRepository
from ..models.airline_staff import AirlineStaff


class Database:
    def __init__(self) -> None:
        self.airlines = AirlineRepository()
        self.airplanes = AirplaneRepository()
        self.dispatchers = DispatcherRepository()
        self.flights = FlightRepository()
        self.attendants = AttendantRepository()
        self.pilots = PilotRepository()
        self.routes = RouteRepository()
        self.airline_staff = AirlineStaffRepository(model_cls=AirlineStaff)
        self.gates = GateRepository()
        self.destinations = DestinationRepository()

        self.gates.set_flight_repo(self.flights)

        self.dispatchers.set_flights(self.flights)

        self.airlines.set_airplane_repo(self.airplanes)
        self.airlines.set_airline_staff_repo(self.airline_staff)

        self.airplanes.set_airline_repo(self.airlines)
        self.airplanes.set_flight_repo(self.flights)

        self.flights.set_airplane_repo(self.airplanes)
        self.flights.set_gate_repo(self.gates)
        self.flights.set_attendant_repo(self.attendants)
        self.flights.set_route_repo(self.routes)
        self.flights.set_dispatcher_repo(self.dispatchers)
        self.flights.set_destination_repo(self.destinations)

        self.attendants.set_flight_repo(self.flights)
        self.pilots.set_flight_repo(self.flights)

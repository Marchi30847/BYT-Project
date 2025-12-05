from __future__ import annotations

# Импорты всех репозиториев
from .route_repository import RouteRepository
from .destination_repository import DestinationRepository
from .attendant_repository import AttendantRepository
from .dispatcher_repository import DispatcherRepository
from .pilot_repository import PilotRepository
from .gate_repository import GateRepository
from .airline_repository import AirlineRepository
from .airline_staff_repository import AirlineStaffRepository
from .airplane_repository import AirplaneRepository
from .flight_repository import FlightRepository
from .employee_repository import EmployeeRepository  # Для полноты
from .terminal_repository import TerminalRepository  # <-- Добавлено
from .security_officer_repository import SecurityOfficerRepository  # Для полноты

from ..models.airline_staff import AirlineStaff
from ..models.employee import Employee


class Database:
    def __init__(self) -> None:
        self.terminals = TerminalRepository()  # <-- Добавлено
        self.gates = GateRepository()
        self.destinations = DestinationRepository()
        self.routes = RouteRepository()

        self.employees = EmployeeRepository(model_cls=Employee)
        self.airline_staff = AirlineStaffRepository(model_cls=AirlineStaff)
        self.security_officers = SecurityOfficerRepository()
        self.attendants = AttendantRepository()
        self.pilots = PilotRepository()
        self.dispatchers = DispatcherRepository()

        self.airlines = AirlineRepository()
        self.airplanes = AirplaneRepository()
        self.flights = FlightRepository()


        self.flights.set_gate_repo(self.gates)
        self.flights.set_attendant_repo(self.attendants)
        self.flights.set_pilot_repo(self.pilots)
        self.flights.set_airplane_repo(self.airplanes)
        self.flights.set_route_repo(self.routes)
        self.flights.set_dispatcher_repo(self.dispatchers)
        self.flights.set_destination_repo(self.destinations)

        self.airlines.set_airplane_repo(self.airplanes)
        self.airlines.set_airline_staff_repo(self.airline_staff)

        self.airplanes.set_airline_repo(self.airlines)
        self.airplanes.set_flight_repo(self.flights)

        self.airline_staff.set_airline_repo(self.airlines)

        self.attendants.set_flight_repo(self.flights)
        self.pilots.set_flight_repo(self.flights)

        self.gates.set_flight_repo(self.flights)

        self.dispatchers.set_flight_repo(self.flights)
        self.dispatchers.set_terminal_repo(self.terminals)

        self.terminals.set_gate_repo(self.gates)
        self.terminals.set_dispatcher_repo(self.dispatchers)
        self.terminals.set_security_officer_repo(self.security_officers)

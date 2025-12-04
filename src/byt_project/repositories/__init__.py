from .base import Database
from .base import BaseRepository

from .base.base_repository import BaseRepository
from .airline_repository import AirlineRepository
from .airplane_repository import AirplaneRepository
from .attendant_repository import AttendantRepository
from .destination_repository import DestinationRepository
from .dispatcher_repository import DispatcherRepository
from .employee_repository import EmployeeRepository
from .flight_repository import FlightRepository
from .gate_repository import GateRepository
from .pilot_repository import PilotRepository
from .route_repository import RouteRepository
from .scanner_operator_repository import ScannerOperatorRepository
from .seat_repository import SeatRepository
from .security_officer_repository import SecurityOfficerRepository
from .terminal_repository import TerminalRepository
from .ticket_repository import TicketRepository


db = Database()

__all__ = [
    "db",
    "Database",

    "BaseRepository",

    "AirlineRepository",
    "AirplaneRepository",
    "AttendantRepository",
    "DestinationRepository",
    "DispatcherRepository",
    "EmployeeRepository",
    "FlightRepository",
    "GateRepository",
    "PilotRepository",
    "RouteRepository",
    "ScannerOperatorRepository",
    "SeatRepository",
    "SecurityOfficerRepository",
    "TerminalRepository",
    "TicketRepository",
]
from __future__ import annotations

from typing import TypeVar, override

from .employee_repository import EmployeeRepository
from .flight_repository import FlightRepository
from .terminal_repository import TerminalRepository
from ..models import Dispatcher

T = TypeVar('T', bound=Dispatcher)


class DispatcherRepository(EmployeeRepository[Dispatcher]):
    def __init__(self) -> None:
        super().__init__(model_cls=Dispatcher)

        self._flight_repo: FlightRepository | None = None
        self._terminal_repo: TerminalRepository | None = None

    def set_flights(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

    @override
    def _inject_dependencies(self, obj: Dispatcher) -> None:
        obj.set_loader("flights", self._flight_repo.find_all_by_dispatcher_id)
        obj.set_loader("terminal", self._terminal_repo.find_by_id)

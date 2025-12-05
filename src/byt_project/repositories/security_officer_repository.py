from __future__ import annotations

from typing import TYPE_CHECKING, override

from .employee_repository import EmployeeRepository
from ..models.security_officer import SecurityOfficer

if TYPE_CHECKING:
    from .incident_repository import IncidentRepository
    from .terminal_repository import TerminalRepository


class SecurityOfficerRepository(EmployeeRepository[SecurityOfficer]):
    def __init__(self) -> None:
        super().__init__(model_cls=SecurityOfficer)

        self._incidents_repo: IncidentRepository | None = None
        self._terminal_repo: TerminalRepository | None = None

    def set_incidents_repo(self, repo: IncidentRepository) -> None:
        self._incidents_repo = repo

    def set_terminal_repo(self, repo: TerminalRepository) -> None:
        self._terminal_repo = repo


    @override
    def _inject_dependencies(self, obj: SecurityOfficer) -> None:
        obj.set_loader("manager", self.find_by_id)

        obj.set_loader("subordinates", self.find_all_by_manager_id)

        if self._terminal_repo:
            obj.set_loader("terminal", self._terminal_repo.find_by_id)

        if self._incidents_repo:
            obj.set_loader("incidents", self._incidents_repo.find_all_by_security_officer_id)


    def find_all_by_manager_id(self, manager_id: int) -> list[SecurityOfficer]:
        return [officer for officer in self.find_all() if officer.manager_id == manager_id]

    def find_all_by_terminal_id(self, terminal_id: int) -> list[SecurityOfficer]:
        return [s for s in self.find_all() if s.terminal_id == terminal_id]

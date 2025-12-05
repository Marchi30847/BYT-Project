from __future__ import annotations

from typing import TypeVar, override

from . import EmployeeRepository
from ..models import SecurityOfficer, Terminal, Airline
from ..models.Incident import Incident

T = TypeVar("T", bound=SecurityOfficer)


class SecurityOfficerRepository(EmployeeRepository[T]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=T
        )

        self._incidents_repo: Incident | None = None
        self._terminal_repo: Terminal | None = None

    @override
    def _inject_dependencies(self, obj: Airline) -> None:
        obj.set_loader("manager", self.find_by_id)
        obj.set_loader("subordinates", self.find_all_by_parent_id)
        obj.set_loader("incidents", self._incidents_repo.find_all_by_incident_id) #TODO: need to create incident_repository

    def find_all_by_parent_id(self, parent_id: int) -> list[SecurityOfficer]:
        officers: list[SecurityOfficer] = self.find_all()

        return [a for a in officers if a.parent_company_id == parent_id]
from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, override

from . import EmployeeRepository
from .base.base_repository import BaseRepository
from ..models.airline_staff import AirlineStaff

if TYPE_CHECKING:
    from .airline_repository import AirlineRepository

T = TypeVar("T", bound=AirlineStaff)


class AirlineStaffRepository(EmployeeRepository[T]):
    def __init__(self) -> None:
        super().__init__(model_cls=T) # Put here T because model_cls used in some methods
        self._airline_repo: AirlineRepository | None = None

    def set_airline_repo(self, repo: AirlineRepository) -> None:
        self._airline_repo = repo

    @override
    def _inject_dependencies(self, staff: T) -> None:
        if self._airline_repo:
            staff.set_loader("airline", self._airline_repo.find_by_id)

    def find_all_by_airline_id(self, airline_id: int) -> list[T]:
        all_staff: list[T] = self.find_all()

        return [staff for staff in all_staff if staff.airline_id == airline_id]

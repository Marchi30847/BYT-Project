from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, override

from .base.base_repository import BaseRepository
from ..models.airline_staff import AirlineStaff

if TYPE_CHECKING:
    from .airline_repository import AirlineRepository

T = TypeVar("T", bound=AirlineStaff)


class AirlineStaffRepository(BaseRepository[T]):
    def __init__(self, model_cls: type[T]) -> None:
        super().__init__(model_cls=model_cls)
        self._airline_repo: AirlineRepository | None = None

    def set_airline_repo(self, repo: AirlineRepository) -> None:
        self._airline_repo = repo

    def _inject_dependencies(self, staff: T) -> None:
        if self._airline_repo:
            staff.set_loader("airline", self._airline_repo.find_by_id)

    @override
    def find_by_id(self, obj_id: int) -> T | None:
        staff_member: T | None = super().find_by_id(obj_id)

        if staff_member:
            self._inject_dependencies(staff_member)

        return staff_member

    @override
    def find_all(self) -> list[T]:
        all_staff: list[T] = super().find_all()

        for staff in all_staff:
            self._inject_dependencies(staff)

        return all_staff

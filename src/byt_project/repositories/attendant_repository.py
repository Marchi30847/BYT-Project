from __future__ import annotations

from typing import TYPE_CHECKING, override

from .airline_staff_repository import AirlineStaffRepository
from ..models.attendant import Attendant

if TYPE_CHECKING:
    from .flight_repository import FlightRepository

class AttendantRepository(AirlineStaffRepository[Attendant]):
    def __init__(self) -> None:
        super().__init__(model_cls=Attendant)

        self._flight_repo: FlightRepository | None = None

    def set_flight_repo(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

    @override
    def _inject_dependencies(self, obj: Attendant) -> None:
        super()._inject_dependencies(obj)

        if self._flight_repo:
            obj.set_loader("flights", self._flight_repo.find_all_by_attendant_id)

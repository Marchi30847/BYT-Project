from __future__ import annotations

from . import FlightRepository
from .airline_staff_repository import AirlineStaffRepository
from .base import BaseRepository
from ..models import Attendant, AirlineStaff


class AttendantRepository(AirlineStaffRepository[Attendant]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Attendant,
        )

        self._flight_repo: FlightRepository | None = None

    def _inject_dependencies(self, obj: Attendant) -> None:
        obj.set_loader("flights", self._flight_repo.find_all_by_attendant_id)

    def set_flight_repo(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

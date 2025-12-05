from __future__ import annotations

from . import FlightRepository
from .airline_staff_repository import AirlineStaffRepository
from ..models import Pilot


class PilotRepository(AirlineStaffRepository[Pilot]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Pilot
        )

        self._flight_repo: FlightRepository | None = None

    def _inject_dependencies(self, obj: Pilot) -> None:
        obj.set_loader("flights", self._flight_repo.find_all_by_pilot_ids)

    def set_flight_repo(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

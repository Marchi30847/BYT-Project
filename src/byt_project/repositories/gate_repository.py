from __future__ import annotations

from typing import override

from .flight_repository import FlightRepository
from .base import BaseRepository
from ..models import Gate


class GateRepository(BaseRepository[Gate]):
    def __init__(self) -> None:
        super().__init__(model_cls=Gate)

        self._flight_repo: FlightRepository | None = None

    def set_flight_repo(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

    @override
    def _inject_dependencies(self, obj: Gate) -> None:
        obj.set_loader("flights", self._flight_repo.find_all_by_gate_id)
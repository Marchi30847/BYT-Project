from __future__ import annotations

from typing import TYPE_CHECKING, override
from .base.base_repository import BaseRepository
from ..models.destination import Destination

if TYPE_CHECKING:
    from .flight_repository import FlightRepository


class DestinationRepository(BaseRepository[Destination]):
    def __init__(self) -> None:
        super().__init__(model_cls=Destination)
        self._flight_repo: FlightRepository | None = None

    def set_flight_repo(self, repo: FlightRepository) -> None:
        self._flight_repo = repo

    @override
    def _inject_dependencies(self, obj: Destination) -> None:
        if self._flight_repo:
            obj.set_loader("flights", self._flight_repo.find_all_by_destination_id)

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .base.base_repository import BaseRepository
from ..models.airplane import Airplane

if TYPE_CHECKING:
    from .airline_repository import AirlineRepository
    from .flight_repository import FlightRepository


class AirplaneRepository(BaseRepository[Airplane]):
    def __init__(self) -> None:
        super().__init__(model_cls=Airplane)
        self._airline_repo: AirlineRepository | None = None
        self._flight_repo: FlightRepository | None = None

    def set_airline_repo(self, repo: AirlineRepository) -> None:
        self._airline_repo = repo

    def set_flight_repo(self, repo: FlightRepository) -> None:
        self._flight_repo = repo

    def find_all_by_airline_id(self, airline_id: int) -> list[Airplane]:
        airplanes: list[Airplane] = self.find_all()

        return [airplane for airplane in airplanes if airplane.airline_id == airline_id]

    @override
    def _inject_dependencies(self, obj: Airplane) -> None:
        obj.set_loader("airline", self._airline_repo.find_by_id)
        obj.set_loader("flights", self._flight_repo.find_all_by_airplane_id)
        #TODO: seat handling


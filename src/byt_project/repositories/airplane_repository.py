from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .base.base_repository import BaseRepository
from ..models.airplane import Airplane

if TYPE_CHECKING:
    from .airline_repository import AirlineRepository
    from .flight_repository import FlightRepository


class AirplaneRepository(BaseRepository[Airplane]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Airplane,
            data_dir=Path("data/airplanes.json"),
        )
        self._airline_repo: AirlineRepository | None = None
        self._flight_repo: FlightRepository | None = None


    def set_airline_repo(self, repo: AirlineRepository) -> None:
        self._airline_repo = repo

    def set_flight_repo(self, repo: FlightRepository) -> None:
        self._flight_repo = repo

    def find_by_id(self, obj_id: int) -> Airplane | None:
        airplane: Airplane = super().find_by_id(obj_id)

        if airplane:
            self._hydrate(airplane)

        return airplane

    def find_all(self) -> list[Airplane]:
        airplanes: list[Airplane] = super().find_all()

        for plane in airplanes:
            self._hydrate(plane)

        return airplanes

    def _hydrate(self, airplane: Airplane) -> None:
        if self._airline_repo and airplane.airline_id is not None:
            airplane.airline = self._airline_repo.find_by_id(airplane.airline_id)

        if self._flight_repo and airplane.id is not None:
            airplane.flights = self._flight_repo.find_all_by_airplane_id(airplane.id)

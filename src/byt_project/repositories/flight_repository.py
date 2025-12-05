from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Flight


class FlightRepository(BaseRepository[Flight]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Flight,
            data_dir=Path("data/flights.json"),
        )

    def find_all_by_attendant_id(self, airline_id: int) -> list[Flight]:
        pass

    def find_all_by_airplane_ids(self, airplane_ids: list[int]) -> list[Flight]:
        pass

    def find_all_by_dispatcher_id(self, dispatcher_id: int) -> list[Flight]:
        pass

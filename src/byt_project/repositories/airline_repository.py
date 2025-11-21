from __future__ import annotations

from pathlib import Path

from src.byt_project.models.airline import Airline
from src.byt_project.repositories.base_repository import BaseRepository


class AirlineRepository(BaseRepository[Airline]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Airline,
            path=Path("data/airlines.json"),
        )
from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.flight import Flight


class FlightRepository(BaseRepository[Flight]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Flight,
            data_dir=Path("data/flights.json"),
        )
from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Airline


class AirlineRepository(BaseRepository[Airline]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Airline,
            path=Path("data/airlines.json"),
        )
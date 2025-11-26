from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.seat import Seat

class SeatRepository(BaseRepository[Seat]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Seat,
            data_dir=Path("data/seats.json"),
        )
from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Seat

class SeatRepository(BaseRepository[Seat]):
    def __init__(self) -> None:
        super().__init__(model_cls=Seat)
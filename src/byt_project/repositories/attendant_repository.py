from __future__ import annotations

from pathlib import Path

from ..models.airplane import Airplane
from .base_repository import BaseRepository
from ..models.attendant import Attendant


class AttendantRepository(BaseRepository[Attendant]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Attendant,
            data_dir=Path("data/attendants.json"),
        )
from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Attendant


class AttendantRepository(BaseRepository[Attendant]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Attendant,
            data_dir=Path("data/attendants.json"),
        )
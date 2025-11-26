from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.pilot import Pilot


class PilotRepository(BaseRepository[Pilot]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Pilot,
            data_dir=Path("data/pilots.json"),
        )
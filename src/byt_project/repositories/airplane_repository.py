from __future__ import annotations

from pathlib import Path

from ..models.airplane import Airplane
from .base_repository import BaseRepository


class AirplaneRepository(BaseRepository[Airplane]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Airplane,
            data_dir=Path("data"),
        )
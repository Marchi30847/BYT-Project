from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.gate import Gate


class GateRepository(BaseRepository[Gate]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Gate,
            data_dir=Path("data/gates.json"),
        )
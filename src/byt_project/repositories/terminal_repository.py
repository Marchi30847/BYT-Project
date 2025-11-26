from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.terminal import Terminal


class TerminalRepository(BaseRepository[Terminal]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Terminal,
            data_dir=Path("data/terminals.json"),
        )
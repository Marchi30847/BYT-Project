from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.dispatcher import Dispatcher


class DispatcherRepository(BaseRepository[Dispatcher]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Dispatcher,
            data_dir=Path("data/dispatchers.json"),
        )
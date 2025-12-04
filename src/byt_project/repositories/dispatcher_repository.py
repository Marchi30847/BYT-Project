from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Dispatcher


class DispatcherRepository(BaseRepository[Dispatcher]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Dispatcher,
            data_dir=Path("data/dispatchers.json"),
        )
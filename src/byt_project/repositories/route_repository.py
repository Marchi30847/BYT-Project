from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Route


class RouteRepository(BaseRepository[Route]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Route,
            data_dir=Path("data/routes.json"),
        )
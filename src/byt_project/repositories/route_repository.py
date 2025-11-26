from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.route import Route


class RouteRepository(BaseRepository[Route]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Route,
            data_dir=Path("data/routes.json"),
        )
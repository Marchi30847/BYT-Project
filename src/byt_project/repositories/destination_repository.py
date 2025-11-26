from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models.destination import Destination


class DestinationRepository(BaseRepository[Destination]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Destination,
            data_dir=Path("data/Destinations.json"),
        )
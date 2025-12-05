from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Destination


class DestinationRepository(BaseRepository[Destination]):
    def __init__(self) -> None:
        super().__init__(model_cls=Destination)
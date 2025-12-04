from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import AirlineStaff


class AirlineStaffRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            model_cls=AirlineStaff,
            data_dir=Path("data/airplanes.json"),
        )

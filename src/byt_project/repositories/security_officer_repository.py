from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import SecurityOfficer


class SecurityOfficerRepository(BaseRepository[SecurityOfficer]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=SecurityOfficer,
            data_dir=Path("data/security_officers.json"),
        )
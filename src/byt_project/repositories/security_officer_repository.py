from __future__ import annotations

from pathlib import Path

from ..models.airplane import Airplane
from .base_repository import BaseRepository
from ..models.security_officer import SecurityOfficer


class SecurityOfficerRepository(BaseRepository[SecurityOfficer]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=SecurityOfficer,
            data_dir=Path("data/security_officers.json"),
        )
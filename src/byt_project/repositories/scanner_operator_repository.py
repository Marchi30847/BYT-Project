from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import ScannerOperator


class ScannerOperatorRepository(BaseRepository[ScannerOperator]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=ScannerOperator,
            data_dir=Path("data/scanner_operators.json"),
        )
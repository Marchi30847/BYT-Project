from __future__ import annotations

from typing import Any

from .base import BaseRepository
from ..models import ScannerOperator


class ScannerOperatorRepository(BaseRepository[ScannerOperator]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=ScannerOperator
        )

        self._scanner_repo: ScannerOperator | None = None

    def find_by_id(self, obj_id: int) -> ScannerOperator | None:
        scanner_operator: ScannerOperator = super().find_by_id(obj_id)

        if scanner_operator:
            self._hydrate(scanner_operator)

        return scanner_operator

    def _hydrate(self, scanner_operator: ScannerOperator) -> None:
        if self._scanner_repo and scanner_operator.scanner_id is not None:
            scanner_operator.scanners = self._scanner_repo.find_all_by_scanner_id(scanner_operator.scanner_id)
            pass




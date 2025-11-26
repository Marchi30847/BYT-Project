from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from . import BaseModel
from .employee import Employee
from .scanner import Scanner


@dataclass
class ScannerOperator(BaseModel, Employee):
    MODEL_TYPE: ClassVar[str] = "scanner_operator"

    authorized_scanner_types: list[str]
    scanners_assigned: list[Scanner]
    incidents_reported: int = 0



    def __post_init__(self) -> None:
        if len(self.authorized_scanner_types) not in (1, 2):
            raise ValueError("ScannerOperator must have 1 or 2 authorized scanner types")

    def report_incident(self, description: str) -> None:
        raise NotImplementedError

    def addAuthorizedScannerType(self, scannerType: str) -> None:
        self.authorized_scanner_types.append(scannerType)
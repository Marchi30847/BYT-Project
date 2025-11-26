from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.byt_project.models import BaseModel
from src.byt_project.models.scanner_operator import ScannerOperator


@dataclass
class Scanner(BaseModel):
    MODEL_TYPE: ClassVar[str] = "scanner"

    model: str
    lastCalibration: datetime
    avgScanTime: float

    operators: list[ScannerOperator]


    def addOperator(self, operator: ScannerOperator) -> None:
        self.operators.append(operator)
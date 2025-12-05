from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from .scanner_operator import ScannerOperator


@dataclass(kw_only=True)
class Scanner(BaseModel):
    MODEL_TYPE: ClassVar[str] = "scanner"

    model: str
    lastCalibration: datetime
    avgScanTime: float

    operators: list[ScannerOperator]

    def __post_init__(self) -> None:
        super().__post_init__()

        # model
        if not isinstance(self.model, str) or not self.model.strip():
            raise ValueError("model must be a non-empty string")

        # lastCalibration
        if not isinstance(self.lastCalibration, datetime):
            raise TypeError("lastCalibration must be a datetime object")

        # avgScanTime
        if not isinstance(self.avgScanTime, (int, float)) or self.avgScanTime <= 0:
            raise ValueError("avgScanTime must be a positive number")

        # operators
        if not isinstance(self.operators, list):
            raise TypeError("operators must be a list")

        for op in self.operators:
            if not isinstance(op, ScannerOperator):
                raise TypeError("all items in operators must be ScannerOperator instances")

    def addOperator(self, operator: ScannerOperator) -> None:
        self.operators.append(operator)
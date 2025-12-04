from dataclasses import dataclass
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.checkedin_luggage import CheckedInLuggage
from src.byt_project.models.scanner import Scanner


@dataclass(kw_only=True)
class BHSSScanner(BaseModel, Scanner):
    MODEL_TYPE: ClassVar[str] = "bhss_scanner"

    belt_id: int
    maxThroughput: int
    isAutoSortEnabled: bool

    scannedLuggage: list[CheckedInLuggage]
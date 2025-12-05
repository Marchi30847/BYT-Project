from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING

from .base import BaseModel
from .scanner import Scanner

if TYPE_CHECKING:
    from .checkedin_luggage import CheckedInLuggage


@dataclass(kw_only=True)
class BHSSScanner(Scanner):
    MODEL_TYPE: ClassVar[str] = "bhss_scanner"

    belt_id: int
    maxThroughput: int
    isAutoSortEnabled: bool

    scannedLuggage: list[CheckedInLuggage]
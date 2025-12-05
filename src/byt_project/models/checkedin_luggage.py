from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, TYPE_CHECKING

from .base import BaseModel
from .luggage import Luggage

if TYPE_CHECKING:
    from .bhss_scanner import BHSSScanner


@dataclass(kw_only=True)
class CheckedInLuggage(Luggage):
    MODEL_TYPE: ClassVar[str] = "carryon_luggage"

    checkedInTime: datetime
    beltNumber: int
    isLoadedToFlight: bool

    scannedIn: BHSSScanner

    def getScanResult(self):
        pass
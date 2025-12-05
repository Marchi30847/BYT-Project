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

    def __post_init__(self) -> None:
        super().__post_init__()

        # checkedInTime
        if not isinstance(self.checkedInTime, datetime):
            raise TypeError("checkedInTime must be a datetime object")

        # beltNumber
        if not isinstance(self.beltNumber, int) or self.beltNumber <= 0:
            raise ValueError("beltNumber must be a positive integer")

        # isLoadedToFlight
        if not isinstance(self.isLoadedToFlight, bool):
            raise TypeError("isLoadedToFlight must be a boolean")

        # scannedIn (BHSSScanner)
        if self.scannedIn is None:
            raise ValueError("scannedIn must not be None")

        from .bhss_scanner import BHSSScanner
        if not isinstance(self.scannedIn, BHSSScanner):
            raise TypeError("scannedIn must be a BHSSScanner instance")

    def getScanResult(self):
        pass
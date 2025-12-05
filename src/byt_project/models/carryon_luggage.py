from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING

from .base import BaseModel
from .luggage import Luggage

if TYPE_CHECKING:
    from .security_scanner import SecurityScanner


@dataclass(kw_only=True)
class CarryOnLuggage(Luggage):
    MODEL_TYPE: ClassVar[str] = "carryon_luggage"

    fitsInCabin: bool
    liquidBagCount: int

    scannedIn: SecurityScanner

    def __post_init__(self) -> None:
        super().__post_init__()

        # fitsInCabin
        if not isinstance(self.fitsInCabin, bool):
            raise TypeError("fitsInCabin must be a boolean")

        # liquidBagCount
        if not isinstance(self.liquidBagCount, int) or self.liquidBagCount < 0:
            raise ValueError("liquidBagCount must be a non-negative integer")

        # scannedIn (SecurityScanner)
        if self.scannedIn is None:
            raise ValueError("scannedIn must not be None")

        if not isinstance(self.scannedIn, SecurityScanner):
            raise TypeError("scannedIn must be a SecurityScanner instance")

    def getScanResult(self):
        pass
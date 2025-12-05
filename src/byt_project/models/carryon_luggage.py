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

    def getScanResult(self):
        pass
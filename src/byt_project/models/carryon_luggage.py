from dataclasses import dataclass
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.luggage import Luggage
from src.byt_project.models.security_scanner import SecurityScanner




@dataclass(kw_only=True)
class CarryOnLuggage(BaseModel, Luggage):
    MODEL_TYPE: ClassVar[str] = "carryon_luggage"

    fitsInCabin: bool
    liquidBagCount: int

    scannedIn: SecurityScanner

    def getScanResult(self):
        pass
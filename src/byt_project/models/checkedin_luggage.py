from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.bhss_scanner import BHSSScanner
from src.byt_project.models.luggage import Luggage




@dataclass(kw_only=True)
class CheckedInLuggage(BaseModel, Luggage):
    MODEL_TYPE: ClassVar[str] = "carryon_luggage"

    checkedInTime: datetime
    beltNumber: int
    isLoadedToFlight: bool

    scannedIn: BHSSScanner

    def getScanResult(self):
        pass
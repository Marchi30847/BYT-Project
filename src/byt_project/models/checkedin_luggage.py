from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.byt_project.models import BaseModel
from src.byt_project.models.bhss_scanner import BHSSScanner
from src.byt_project.models.luggage import Luggage
from src.byt_project.models.security_scanner import SecurityScanner




@dataclass
class CheckedInLuggage(BaseModel, Luggage):
    MODEL_TYPE: ClassVar[str] = "carryon_luggage"

    checkedInTime: datetime
    beltNumber: int
    isLoadedToFlight: bool

    scannedIn: BHSSScanner

    def getScanResult(self):
        pass
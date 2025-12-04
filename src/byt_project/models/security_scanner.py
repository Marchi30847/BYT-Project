from dataclasses import dataclass
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.bhss_scanner import Scanner
from src.byt_project.models.carryon_luggage import CarryOnLuggage


@dataclass(kw_only=True)
class SecurityScanner(BaseModel, Scanner):
    MODEL_TYPE: ClassVar[str] = "security_scanner"

    xray_intensity: float
    supports_3d_scan: bool

    scannedLuggage: list[CarryOnLuggage]

    def __post_init__(self) -> None:
        if self.xray_intensity < 0 or self.xray_intensity > 1:
            raise ValueError("Xray intensity must be between 0 and 1")

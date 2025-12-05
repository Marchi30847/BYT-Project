from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING

from .base import BaseModel
from .bhss_scanner import Scanner

if TYPE_CHECKING:
    from .carryon_luggage import CarryOnLuggage


@dataclass(kw_only=True)
class SecurityScanner(Scanner):
    MODEL_TYPE: ClassVar[str] = "security_scanner"

    xray_intensity: float
    supports_3d_scan: bool

    scannedLuggage: list[CarryOnLuggage]

    def __post_init__(self) -> None:
        if self.xray_intensity < 0 or self.xray_intensity > 1:
            raise ValueError("Xray intensity must be between 0 and 1")

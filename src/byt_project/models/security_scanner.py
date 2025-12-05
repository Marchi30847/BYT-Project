from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING

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
        super().__post_init__()

        # xray_intensity: must be between 0 and 1
        if not isinstance(self.xray_intensity, (int, float)):
            raise TypeError("SecurityScanner.xray_intensity must be a number")

        if not (0 <= self.xray_intensity <= 1):
            raise ValueError("SecurityScanner.xray_intensity must be between 0 and 1")

        # supports_3d_scan
        if not isinstance(self.supports_3d_scan, bool):
            raise TypeError("SecurityScanner.supports_3d_scan must be a boolean")
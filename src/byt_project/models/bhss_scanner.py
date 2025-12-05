from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING

from .scanner import Scanner

if TYPE_CHECKING:
    from .checkedin_luggage import CheckedInLuggage


@dataclass(kw_only=True)
class BHSSScanner(Scanner):
    MODEL_TYPE: ClassVar[str] = "bhss_scanner"

    belt_id: int
    maxThroughput: int
    isAutoSortEnabled: bool

    scannedLuggage: list[CheckedInLuggage]

    def __post_init__(self) -> None:
        super().__post_init__()

        # belt_id
        if not isinstance(self.belt_id, int) or self.belt_id <= 0:
            raise ValueError("belt_id must be a positive integer")

        # maxThroughput
        if not isinstance(self.maxThroughput, int) or self.maxThroughput <= 0:
            raise ValueError("maxThroughput must be a positive integer")

        # isAutoSortEnabled
        if not isinstance(self.isAutoSortEnabled, bool):
            raise TypeError("isAutoSortEnabled must be a boolean")


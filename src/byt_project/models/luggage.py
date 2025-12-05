from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, TYPE_CHECKING

from src.byt_project.models.base import BaseModel

if TYPE_CHECKING:
    from src.byt_project.models.ticket import Ticket


class SecurityStatus(str, Enum):
    NOT_FLAGGED = "Not flagged"
    SCANNED = "Scanned"
    FLAGGED = "Flagged"
    CLEARED = "Cleared"

@dataclass(kw_only=True)
class Luggage(BaseModel):
    MODEL_TYPE: ClassVar[str] = "luggage"

    weight: int
    dimensions: str
    isFragile: bool
    securityStatus: SecurityStatus
    ticket: Ticket

    def __post_init__(self) -> None:
        super().__post_init__()

        # weight
        if not isinstance(self.weight, (int, float)) or self.weight <= 0:
            raise ValueError("weight must be a positive number")

        # dimensions
        if not isinstance(self.dimensions, str) or not self.dimensions.strip():
            raise ValueError("dimensions must be a non-empty string")

        # isFragile
        if not isinstance(self.isFragile, bool):
            raise TypeError("isFragile must be a boolean")

        # securityStatus
        if not isinstance(self.securityStatus, SecurityStatus):
            raise TypeError("securityStatus must be a SecurityStatus enum value")

        # ticket (required relation)
        if self.ticket is None:
            raise ValueError("ticket must not be None")

        # Optional soft check: ensure ticket is correct type
        if not isinstance(self.ticket, Ticket):
            raise TypeError("ticket must be a Ticket instance")

    def checkIn(self):
        pass

    def weight(self):
        pass
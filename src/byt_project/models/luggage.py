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

    def checkIn(self):
        pass

    def weight(self):
        pass
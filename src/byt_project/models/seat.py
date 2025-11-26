from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from .base import BaseModel
from .ticket import Ticket


@dataclass
class Seat(BaseModel):
    MODEL_TYPE: ClassVar[str] = "seat"

    number: int
    row_letter: str
    ticket: Ticket

    def assign_ticket(self, ticket) -> None:
        if self.ticket is not None:
            raise ValueError("Seat already assigned to another ticket")

        self.ticket = ticket

    def is_available(self) -> bool:
        return self.ticket is None
from __future__ import annotations

from pathlib import Path

from .base import BaseRepository
from ..models import Ticket


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Ticket,
            data_dir=Path("data/tickets.json"),
        )
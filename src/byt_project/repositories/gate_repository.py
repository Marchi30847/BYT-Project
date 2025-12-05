from __future__ import annotations

from typing import TYPE_CHECKING, override
from .base.base_repository import BaseRepository
from ..models.gate import Gate

if TYPE_CHECKING:
    from .flight_repository import FlightRepository
    from .terminal_repository import TerminalRepository


class GateRepository(BaseRepository[Gate]):
    def __init__(self) -> None:
        super().__init__(model_cls=Gate)

        self._flight_repo: FlightRepository | None = None
        self._terminal_repo: TerminalRepository | None = None

    def set_flight_repo(self, flight_repo: FlightRepository) -> None:
        self._flight_repo = flight_repo

    def set_terminal_repo(self, terminal_repo: TerminalRepository) -> None:
        self._terminal_repo = terminal_repo

    @override
    def _inject_dependencies(self, obj: Gate) -> None:
        if self._terminal_repo:
            obj.set_loader("terminal", self._terminal_repo.find_by_id)

        if self._flight_repo:
            obj.set_loader("flights", self._flight_repo.find_all_by_gate_id)

    def find_all_by_terminal_id(self, terminal_id: int) -> list[Gate]:
        return [g for g in self.find_all() if g.terminal_id == terminal_id]

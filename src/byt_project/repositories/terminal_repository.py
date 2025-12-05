from __future__ import annotations

from typing import TYPE_CHECKING, override
from .base import BaseRepository
from ..models import Terminal

if TYPE_CHECKING:
    from .dispatcher_repository import DispatcherRepository
    from .security_officer_repository import SecurityOfficerRepository
    from .gate_repository import GateRepository


class TerminalRepository(BaseRepository[Terminal]):
    def __init__(self) -> None:
        super().__init__(model_cls=Terminal)

        self._dispatcher_repo: DispatcherRepository | None = None
        self._security_officer_repo: SecurityOfficerRepository | None = None
        self._gate_repo: GateRepository | None = None

    def set_dispatcher_repo(self, repo: DispatcherRepository) -> None:
        self._dispatcher_repo = repo

    def set_security_officer_repo(self, repo: SecurityOfficerRepository) -> None:
        self._security_officer_repo = repo

    def set_gate_repo(self, repo: GateRepository) -> None:
        self._gate_repo = repo

    @override
    def _inject_dependencies(self, obj: Terminal) -> None:
        if self._dispatcher_repo:
            obj.set_loader("dispatchers", self._dispatcher_repo.find_all_by_terminal_id)
        if self._security_officer_repo:
            obj.set_loader("security_officers", self._security_officer_repo.find_all_by_terminal_id)
        if self._gate_repo:
            obj.set_loader("gates", self._gate_repo.find_all_by_terminal_id)

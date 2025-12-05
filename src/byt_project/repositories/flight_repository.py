from __future__ import annotations

from pathlib import Path

from typing import TYPE_CHECKING, override

from .base import BaseRepository
from ..models import Flight

if TYPE_CHECKING:
    from .gate_repository import GateRepository
    from .pilot_repository import PilotRepository
    from .attendant_repository import AttendantRepository
    from .airplane_repository import AirplaneRepository
    from .route_repository import RouteRepository
    from .dispatcher_repository import DispatcherRepository
    from .destination_repository import DestinationRepository

class FlightRepository(BaseRepository[Flight]):
    def __init__(self) -> None:
        super().__init__(model_cls=Flight)

        self._gate_repo: GateRepository | None = None
        self._pilot_repo: PilotRepository | None = None
        self._attendant_repo: AttendantRepository | None = None
        self._airplane_repo: AirplaneRepository | None = None
        self._route_repo: RouteRepository | None = None
        self._dispatcher_repo: DispatcherRepository | None = None
        self._destination_repo: DestinationRepository | None = None

    def set_gate_repo(self, repo: GateRepository) -> None:
        self._gate_repo = repo

    def set_pilot_repo(self, repo: PilotRepository) -> None:
        self._pilot_repo = repo

    def set_attendant_repo(self, repo: AttendantRepository) -> None:
        self._attendant_repo = repo

    def set_airplane_repo(self, repo: AirplaneRepository) -> None:
        self._airplane_repo = repo

    def set_route_repo(self, repo: RouteRepository) -> None:
        self._route_repo = repo

    def set_dispatcher_repo(self, repo: DispatcherRepository) -> None:
        self._dispatcher_repo = repo

    def set_destination_repo(self, repo: DestinationRepository) -> None:
        self._destination_repo = repo

    @override
    def _inject_dependencies(self, obj: Flight) -> None:
        if self._gate_repo:
            obj.set_loader("gate", self._gate_repo.find_by_id)

        if self._pilot_repo:
            obj.set_loader("pilots", lambda ids: [p for i in ids if (p := self._pilot_repo.find_by_id(i))])

        if self._attendant_repo:
            obj.set_loader("attendants", lambda ids: [a for i in ids if (a := self._attendant_repo.find_by_id(i))])

        if self._airplane_repo:
            obj.set_loader("airplane", self._airplane_repo.find_by_id)

        if self._route_repo:
            obj.set_loader("route", self._route_repo.find_by_id)

        if self._dispatcher_repo:
            obj.set_loader("dispatcher", self._dispatcher_repo.find_by_id)

        if self._destination_repo:
            obj.set_loader("destination", self._destination_repo.find_by_id)


    def find_all_by_attendant_id(self, attendant_id: int) -> list[Flight]:
        return [f for f in self.find_all() if attendant_id in f.attendant_ids]

    def find_all_by_airplane_ids(self, airplane_ids: list[int]) -> list[Flight]:
        return [f for f in self.find_all() if f.airplane_id in airplane_ids]

    def find_all_by_airplane_id(self, airplane_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.airplane_id == airplane_id]

    def find_all_by_dispatcher_id(self, dispatcher_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.dispatcher_id == dispatcher_id]

    def find_all_by_pilot_id(self, pilot_id: int) -> list[Flight]:
        return [f for f in self.find_all() if pilot_id in f.pilot_ids]

    def find_all_by_gate_id(self, gate_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.gate_id == gate_id]

    def find_all_by_destination_id(self, destination_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.destination_id == destination_id]

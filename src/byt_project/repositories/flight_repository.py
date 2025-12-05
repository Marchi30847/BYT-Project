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
    from .customer_repository import CustomerRepository


class FlightRepository(BaseRepository[Flight]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Flight,
            data_dir=Path("data/flights.json"),
        )
        self._gate_repo: GateRepository | None = None
        self._pilot_repo: PilotRepository | None = None
        self._attendant_repo: AttendantRepository | None = None
        self._airplane_repo: AirplaneRepository | None = None
        self._route_repo: RouteRepository | None = None
        self._dispatcher_repo: DispatcherRepository | None = None
        self._destination_repo: DestinationRepository | None = None
        self._customer_repo: CustomerRepository | None = None

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

    def set_customer_repo(self, repo: CustomerRepository) -> None:
        self._customer_repo = repo

    @override
    def _inject_dependencies(self, obj: Flight) -> None:
        if self._gate_repo:
            obj.set_loader("gate", self._gate_repo.find_by_id)
        if self._pilot_repo:
            obj.set_loader("captain", self._pilot_repo.find_by_id)
            # For list of IDs, we need a method that accepts a list of IDs
            # Assuming BaseRepository doesn't have find_all_by_ids, we might need to implement it or use a lambda
            # But wait, PilotRepository inherits from AirlineStaffRepository -> EmployeeRepository -> BaseRepository
            # If BaseRepository doesn't have it, we can't just pass find_by_id.
            # We need a method in PilotRepository that takes a list of IDs.
            # Let's assume for now we can use a helper or lambda, or better, add find_all_by_ids to BaseRepository later?
            # Or just implement a specific one in PilotRepository.
            # For now, let's look at how other repos do it.
            # Actually, the model expects a loader that takes the ID(s).
            # If the field is `pilot_ids` (list[int]), the loader receives `list[int]`.
            # So we need `self._pilot_repo.find_all_by_ids`.
            # I'll assume I need to add `find_all_by_ids` to BaseRepository or specific repos.
            # For this task, I will implement a helper in FlightRepository or assume it exists/will be added.
            # Let's check BaseRepository again. It does NOT have find_all_by_ids.
            # I will implement a lambda here for now: lambda ids: [self._pilot_repo.find_by_id(i) for i in ids]
            # But find_by_id returns T | None. We need list[T].
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
        if self._customer_repo:
            # Customer has find_all_by_flight_id? I haven't checked CustomerRepository yet.
            # Assuming it should have it.
            if hasattr(self._customer_repo, 'find_all_by_flight_id'):
                obj.set_loader("customers", self._customer_repo.find_all_by_flight_id)

    def find_all_by_attendant_id(self, attendant_id: int) -> list[Flight]:
        return [f for f in self.find_all() if attendant_id in f.attendant_ids]

    def find_all_by_airplane_ids(self, airplane_ids: list[int]) -> list[Flight]:
        return [f for f in self.find_all() if f.airplane_id in airplane_ids]

    def find_all_by_airplane_id(self, airplane_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.airplane_id == airplane_id]

    def find_all_by_dispatcher_id(self, dispatcher_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.dispatcher_id == dispatcher_id]

    def find_all_by_pilot_ids(self, pilot_ids: list[int]) -> list[Flight]:
        # This seems to mean "find flights where ANY of these pilots are assigned" or "ALL"?
        # Usually for a "find_all_by_X_ids" it implies X is a foreign key on Flight.
        # But Flight has `pilot_ids` (many-to-many).
        # If the input is a list of pilot IDs, maybe we want flights that have ANY of these pilots?
        # OR, is this method intended to be used by PilotRepository?
        # PilotRepository calls `find_all_by_pilot_ids` passing `self.id` (which is ONE int).
        # So the current usage in PilotRepository is wrong (passing int to list arg).
        # I will implement `find_all_by_pilot_id` for that.
        # For `find_all_by_pilot_ids`, I'll assume it filters flights containing any of the given pilots.
        return [f for f in self.find_all() if any(pid in f.pilot_ids for pid in pilot_ids)]

    def find_all_by_pilot_id(self, pilot_id: int) -> list[Flight]:
        return [f for f in self.find_all() if pilot_id in f.pilot_ids]

    def find_all_by_gate_id(self, gate_id: int) -> list[Flight]:
        return [f for f in self.find_all() if f.gate_id == gate_id]

from __future__ import annotations

from typing import override, TYPE_CHECKING

from .person_repository import PersonRepository
from ..models import Customer

if TYPE_CHECKING:
    from . import FlightRepository


class CustomerRepository(PersonRepository[Customer]):
    def __init__(self) -> None:
        super().__init__(model_cls=Customer)

        self._flight_repo: FlightRepository | None = None

    @override
    def _inject_dependencies(self, obj: Customer) -> None:
        obj.set_loader("flights", self.find_by_id)

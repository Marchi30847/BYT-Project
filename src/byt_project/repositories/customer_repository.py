from __future__ import annotations

from typing import TypeVar, override, Type

from . import FlightRepository
from .person_repository import PersonRepository
from ..models import Employee, Customer

T = TypeVar('T', bound=Employee)


class CustomerRepository(PersonRepository[T]):
    def __init__(self, model_cls: Type[T]) -> None:
        super().__init__(model_cls=model_cls)

        self._flight_repo: FlightRepository | None = None

    @override
    def _inject_dependencies(self, obj: Customer) -> None:
        obj.set_loader("flights", self.find_by_id)

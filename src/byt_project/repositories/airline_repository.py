from __future__ import annotations

from typing import TYPE_CHECKING, override

from .base.base_repository import BaseRepository
from ..models.airline import Airline

if TYPE_CHECKING:
    from .airplane_repository import AirplaneRepository


class AirlineRepository(BaseRepository[Airline]):
    def __init__(self) -> None:
        super().__init__(model_cls=Airline)
        self._airplane_repo: AirplaneRepository | None = None

    def set_airplane_repo(self, airplane_repo: AirplaneRepository) -> None:
        self._airplane_repo = airplane_repo

    def _inject_dependencies(self, obj: Airline) -> None:
        obj.set_loader("parent_company", self.find_by_id)
        obj.set_loader("subcompanies", self.find_all_by_parent_id)
        if self._airplane_repo:
            obj.set_loader("airplanes", self._airplane_repo.find_all_by_airline_id)

    @override
    def find_by_id(self, obj_id: int) -> Airline | None:
        airline: Airline | None = super().find_by_id(obj_id)

        if airline is not None:
            self._inject_dependencies(airline)

        return airline

    @override
    def find_all(self) -> list[Airline]:
        airlines: list[Airline] = super().find_all()

        for airline in airlines:
            self._inject_dependencies(airline)

        return airlines

    def find_all_by_parent_id(self, parent_id: int) -> list[Airline]:
        airlines: list[Airline] = self.find_all()

        return [a for a in airlines if a.parent_company_id == parent_id]

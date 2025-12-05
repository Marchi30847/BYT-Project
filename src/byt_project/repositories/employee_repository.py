from __future__ import annotations

from pathlib import Path
from typing import TypeVar

from .airline_staff_repository import AirlineStaffRepository
from .base import BaseRepository
from ..models import Employee

T = TypeVar('T', bound=Employee)


class EmployeeRepository(BaseRepository[T]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=T
        )

        self._airline_repo = AirlineStaffRepository()


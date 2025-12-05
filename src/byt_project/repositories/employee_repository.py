from __future__ import annotations

from typing import TypeVar

from .person_repository import PersonRepository
from ..models import Employee

T = TypeVar('T', bound=Employee)


class EmployeeRepository(PersonRepository[T]):
    def __init__(self, model_cls: type[T]) -> None:
        super().__init__(
            model_cls=model_cls
        )

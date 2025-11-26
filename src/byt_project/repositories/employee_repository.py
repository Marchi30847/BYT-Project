from __future__ import annotations

from pathlib import Path

from .base_repository import BaseRepository
from ..models import Employee


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self) -> None:
        super().__init__(
            model_cls=Employee,
            data_dir=Path("data/employees.json"),
        )
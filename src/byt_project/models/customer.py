from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.person import Person


@dataclass
class Customer(BaseModel, Person):
    MODEL_TYPE: ClassVar[str] = "customer"

    email: str
    proneNumber: str

    def selfCheckIn(self):
        pass

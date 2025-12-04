from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from src.byt_project.models.base import BaseModel


@dataclass
class Person(BaseModel):
    MODEL_TYPE: ClassVar[str] = "person"

    name: str
    surname: str
    dateOfBirth: date
    gender: str
    nationality: str
    passportNumber: str
    middleName: str | None = None

    def get_age(self) -> int:
        today = date.today()
        years = today.year - self.dateOfBirth.year

        if (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day):
            years -= 1

        return years

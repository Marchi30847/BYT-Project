from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import ClassVar, Any, cast

from .base import BaseModel


@dataclass(kw_only=True)
class Person(BaseModel):
    MODEL_TYPE: ClassVar[str] = "person"

    name: str
    surname: str
    dateOfBirth: date
    gender: str
    nationality: str
    passportNumber: str
    middleName: str | None = None


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data["dateOfBirth"] = self.dateOfBirth.isoformat()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Person:
        data_copy = dict(data)

        raw_dob: Any = data_copy.get("dateOfBirth")
        if isinstance(raw_dob, str):
            data_copy["dateOfBirth"] = date.fromisoformat(raw_dob)

        instance = cast(Person, super().from_dict(data_copy))

        return instance

    def get_age(self) -> int:
        today = date.today()
        years = today.year - self.dateOfBirth.year

        if (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day):
            years -= 1

        return years

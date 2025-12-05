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

        # name
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")

        # surname
        if not isinstance(self.surname, str) or not self.surname.strip():
            raise ValueError("surname must be a non-empty string")

        # middleName — optional, but if provided must be a string
        if self.middleName is not None and not isinstance(self.middleName, str):
            raise TypeError("middleName must be a string or None")

        # dateOfBirth
        if not isinstance(self.dateOfBirth, date):
            raise TypeError("dateOfBirth must be a date object")

        # date must be in the past
        if self.dateOfBirth >= date.today():
            raise ValueError("dateOfBirth must be a past date")

        # gender — simple non-empty string
        if not isinstance(self.gender, str) or not self.gender.strip():
            raise ValueError("gender must be a non-empty string")

        # nationality
        if not isinstance(self.nationality, str) or not self.nationality.strip():
            raise ValueError("nationality must be a non-empty string")

        # passportNumber
        if not isinstance(self.passportNumber, str) or not self.passportNumber.strip():
            raise ValueError("passportNumber must be a non-empty string")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["dateOfBirth"] = self.dateOfBirth.isoformat()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Person:
        data_copy: dict[str, Any] = dict(data)

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

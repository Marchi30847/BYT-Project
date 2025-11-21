from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from .base import BaseModel
from .airline import Airline


@dataclass
class Airplane(BaseModel):
    MODEL_TYPE: ClassVar[str] = "airplane"

    model: str
    manufacturer: str
    capacity: int
    max_luggage_weight: float
    year_of_manufacture: int
    airline: Airline

    max_service_years: ClassVar[int] = 30

    def years_in_service(self) -> int:
        return datetime.now().year - self.year_of_manufacture

    def is_expired(self) -> bool:
        return self.years_in_service() > self.max_service_years
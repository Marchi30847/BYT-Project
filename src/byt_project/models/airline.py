from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .airplane import Airplane
from .base import BaseModel


@dataclass
class Airline(BaseModel):
    MODEL_TYPE: ClassVar[str] = "airline"

    name: str
    iata_code: str
    icao_code: str
    country: str
    fleet_size: int
    airplanes: list[Airplane]
    alliance: str | None
    max_delay_compensation: float = 0.40
    subcompanies: list[Airline] | None = None

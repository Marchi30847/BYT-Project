from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from .base import BaseModel
from .destination import Destination
from .flight import Flight


@dataclass
class Route(BaseModel):
    MODEL_TYPE: ClassVar[str] = "route"

    routeId: str
    destination: Destination
    flight: Flight
    duration: float = 0.0
    distance: float = 0.0

    def __post_init__(self):
        self.is_international = (
            self.destination_from.location.country !=
            self.destination_to.location.country
        )

    def isInternational(self):
        pass
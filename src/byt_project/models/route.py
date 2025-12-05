from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .base import BaseModel
from .destination import Destination
from .flight import Flight


@dataclass(kw_only=True)
class Route(BaseModel):
    MODEL_TYPE: ClassVar[str] = "route"

    routeId: str
    destination: Destination
    flight: Flight
    duration: float = 0.0
    distance: float = 0.0

    def __post_init__(self) -> None:
        super().__post_init__()

        # routeId
        if not isinstance(self.routeId, str) or not self.routeId.strip():
            raise ValueError("routeId must be a non-empty string")

        # destination
        if self.destination is None:
            raise ValueError("destination cannot be None")

        # flight
        if self.flight is None:
            raise ValueError("flight cannot be None")

        # duration
        if not isinstance(self.duration, (int, float)) or self.duration < 0:
            raise ValueError("duration must be a non-negative number")

        # distance
        if not isinstance(self.distance, (int, float)) or self.distance < 0:
            raise ValueError("distance must be a non-negative number")

    def isInternational(self):
        pass
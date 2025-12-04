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


    def isInternational(self):
        pass
from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from .base import BaseModel
from .destination import Destination


@dataclass
class Route(BaseModel):
    MODEL_TYPE: ClassVar[str] = "route"

    routed: str
    destination_from: Destination
    destination_to: Destination

    duration: float = 0.0
    distance: float = 0.0
    is_international: bool = field(init=False)

    def __post_init__(self):
        self.is_international = (
            self.destination_from.location.country !=
            self.destination_to.location.country
        )

    def __repr__(self):
        inter = "International" if self.is_international else "Domestic"
        return f"Route({self.routed}, {inter})"
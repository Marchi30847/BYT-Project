from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.luggage import Luggage

class IncidentType(Enum):
    ILLEGAL_TRANSPORT = "Illegal transport"
    EXPLOSIVE_THREAT = "Explosive threat"


@dataclass(kw_only=True)
class Incident(BaseModel):
    MODEL_TYPE: ClassVar[str] = "incident"

    description: str
    type: IncidentType
    luggage: Luggage

    def __post_init__(self) -> None:
        super().__post_init__()

        # description
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("description must be a non-empty string")

        # type
        if not isinstance(self.type, IncidentType):
            raise TypeError("type must be an IncidentType enum value")

        # luggage
        if self.luggage is None:
            raise ValueError("luggage cannot be None")

        if not isinstance(self.luggage, Luggage):
            raise TypeError("luggage must be a Luggage instance")



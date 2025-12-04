from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from src.byt_project.models.base import BaseModel
from src.byt_project.models.luggage import Luggage

class IncidentType(Enum):
    ILLEGAL_TRANSPORT = "Illegal transport"
    EXPLOSIVE_THREAT = "Explosive threat"


@dataclass
class Incident(BaseModel):
    MODEL_TYPE: ClassVar[str] = "incident"

    description: str
    type: IncidentType
    luggage: Luggage

    @classmethod
    def createIncident(self, desc, type, luggage):
        return Incident(desc, type, luggage)

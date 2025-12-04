from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from src.byt_project.models import BaseModel
from src.byt_project.models.security_officer import SecurityOfficer

class SpecializationArea(Enum):
    CURRENCY = "Currency"
    DRUGS = "Drugs"
    ARTIFACTS = "Artifacts"
    ELECTRONICS = "Electronics"

@dataclass(kw_only=True)
class Attendant(BaseModel, SecurityOfficer):
    MODEL_TYPE: ClassVar[str] = "anti_smuggling_specialist"

    specializationArea: SpecializationArea


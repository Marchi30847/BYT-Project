from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.byt_project.models import BaseModel
from src.byt_project.models.security_officer import SecurityOfficer


@dataclass
class Attendant(BaseModel, SecurityOfficer):
    MODEL_TYPE: ClassVar[str] = "dangerous_goods_qualified"

    licenceNumber: str
    validUntil: datetime
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping, Any, Self

from .base import BaseModel


@dataclass
class Location:
    country: str
    city: str
    latitude: float
    longitude: float


@dataclass
class Destination(BaseModel):
    MODEL_TYPE: ClassVar[str] = "destination"

    name: str
    location: Location
    airport: str

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        kwargs = dict(data)
        kwargs.pop("type", None)
        id_ = kwargs.pop("id", None)

        loc_data = kwargs.get("location")
        if isinstance(loc_data, dict):
            kwargs["location"] = Location(**loc_data)

        obj = cls(**kwargs)
        obj.id = id_
        return obj
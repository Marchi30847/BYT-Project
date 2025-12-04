from __future__ import annotations

from dataclasses import dataclass, fields
from typing import ClassVar, Any, cast

from .base import BaseModel


@dataclass(kw_only=True)
class Location:
    country: str
    city: str
    latitude: float
    longitude: float


@dataclass(kw_only=True)
class Destination(BaseModel):
    MODEL_TYPE: ClassVar[str] = "destination"

    name: str
    location: Location
    airport: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Destination:
        data_copy: dict[str, Any] = dict(data)

        loc_data: dict[str, Any] = data_copy.get("location")

        if isinstance(loc_data, dict):
            loc_valid_fields: set[str] = {f.name for f in fields(Location)}
            clean_loc_data: dict[str, Any] = {k: v for k, v in loc_data.items() if k in loc_valid_fields}

            data_copy["location"] = Location(**clean_loc_data)

        instance = cast(Destination, super().from_dict(data_copy))

        return instance

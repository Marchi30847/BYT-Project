from __future__ import annotations

from dataclasses import dataclass, fields
from typing import ClassVar, Any, TYPE_CHECKING

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
    def from_dict(cls, data: dict[str, Any]) -> Destination:
        valid_arg_names = {f.name for f in fields(cls) if f.init}
        clean_kwargs = {k: v for k, v in data.items() if k in valid_arg_names}

        loc_data = clean_kwargs.get("location")

        if isinstance(loc_data, dict):
            loc_fields = {f.name for f in fields(Location)}
            clean_loc_data = {k: v for k, v in loc_data.items() if k in loc_fields}

            clean_kwargs["location"] = Location(**clean_loc_data)

        instance = cls(**clean_kwargs)

        raw_id: str | int | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        return instance

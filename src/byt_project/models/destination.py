from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import ClassVar, Any, cast, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .flight import Flight


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

    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        # country
        if not isinstance(self.country, str) or not self.country.strip():
            raise ValueError("country must be a non-empty string")

        # city
        if not isinstance(self.city, str) or not self.city.strip():
            raise ValueError("city must be a non-empty string")

        # latitude
        if not isinstance(self.latitude, (int, float)):
            raise TypeError("latitude must be a number")

        if not (-90 <= self.latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")

        # longitude
        if not isinstance(self.longitude, (int, float)):
            raise TypeError("longitude must be a number")

        if not (-180 <= self.longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")

    @property
    def flights(self) -> list[Flight]:
        if self._flights is not None:
            return self._flights

        if self.id is not None:
            loaded: list[Flight] | None = self._run_loader("flights", self.id)
            if loaded is not None:
                self._flights = loaded
                return self._flights

        self._flights = []
        return self._flights

    @flights.setter
    def flights(self, value: list[Flight]) -> None:
        self._flights = value


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Destination:
        data_copy: dict[str, Any] = dict(data)

        raw_loc_data: Any = data_copy.get("location")
        if isinstance(raw_loc_data, dict):
            loc_valid_fields: set[str] = {f.name for f in fields(Location)}
            clean_loc_data: dict[str, Any] = {k: v for k, v in raw_loc_data.items() if k in loc_valid_fields}

            data_copy["location"] = Location(**clean_loc_data)

        instance = cast(Destination, super().from_dict(data_copy))

        return instance

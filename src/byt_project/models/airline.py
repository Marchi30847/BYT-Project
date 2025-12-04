from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .airplane import Airplane


@dataclass(kw_only=True)
class Airline(BaseModel):
    MODEL_TYPE: ClassVar[str] = "airline"

    name: str
    iata_code: str
    icao_code: str
    country: str
    alliance: str | None = None

    parent_company_id: int | None = field(default=None, init=False)
    parent_company: Airline | None = field(default=None)

    airplanes: list[Airplane] = field(default_factory=list)
    subcompanies: list[Airline] = field(default_factory=list)

    max_delay_compensation: ClassVar[float] = 0.40

    def __post_init__(self) -> None:
        if self.parent_company and getattr(self.parent_company, 'id', None) is not None:
            self.parent_company_id = self.parent_company.id

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.parent_company:
            data["parent_company_id"] = self.parent_company.id
        elif self.parent_company_id is not None:
            data["parent_company_id"] = self.parent_company_id
        else:
            data["parent_company_id"] = None

        data.pop("airplanes", None)
        data.pop("subcompanies", None)
        data.pop("parent_company", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Airline:
        instance = cast(Airline, super().from_dict(data))

        raw_parent_id: str | int | None = data.get("parent_company_id")
        instance.parent_company_id = int(raw_parent_id) if raw_parent_id is not None else None

        return instance

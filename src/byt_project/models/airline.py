from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import ClassVar, Any, TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .airplane import Airplane


@dataclass
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
        else:
            data["parent_company_id"] = None

        data.pop("airplanes", None)
        data.pop("subcompanies", None)
        data.pop("parent_company", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Airline:
        valid_arg_names: set[str] = {f.name for f in fields(cls) if f.init}
        clean_kwargs: dict[str, Any] = {k: v for k, v in data.items() if k in valid_arg_names}

        instance = cls(**clean_kwargs)

        raw_parent_id: str | int | None = data.get("parent_company_id")
        instance.parent_company_id = int(raw_parent_id) if raw_parent_id is not None else None

        raw_id: str | int | None = data.get("id")
        instance.id = int(raw_id) if raw_id is not None else None

        return instance

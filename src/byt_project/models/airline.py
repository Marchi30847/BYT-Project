from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .airplane import Airplane
    from .airline_staff import AirlineStaff


@dataclass(kw_only=True)
class Airline(BaseModel):
    MODEL_TYPE: ClassVar[str] = "airline"

    name: str
    iata_code: str
    icao_code: str
    country: str
    alliance: str | None = None

    parent_company_id: int | None = field(default=None, init=False)
    _parent_company: Airline | None = field(default=None, init=False, repr=False)

    _airplanes: list[Airplane] | None = field(default=None, init=False, repr=False)
    _subcompanies: list[Airline] | None = field(default=None, init=False, repr=False)
    _airline_staff: list[AirlineStaff] | None = field(default=None, init=False, repr=False)

    max_delay_compensation: ClassVar[float] = 0.40

    def __post_init__(self) -> None:
        super().__post_init__()

        # name
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")

        # country
        if not isinstance(self.country, str) or not self.country.strip():
            raise ValueError("country must be a non-empty string")

        # alliance
        if self.alliance is not None and not isinstance(self.alliance, str):
            raise TypeError("alliance must be a string or None")

        # IATA code: 2 letters
        if not isinstance(self.iata_code, str) or len(self.iata_code) != 2:
            raise ValueError("iata_code must be exactly 2 characters")
        # no strict alpha enforcement — чтобы не усложнять

        # ICAO code: 3 letters
        if not isinstance(self.icao_code, str) or len(self.icao_code) != 3:
            raise ValueError("icao_code must be exactly 3 characters")

    @property
    def parent_company(self) -> Airline | None:
        if self._parent_company is not None:
            return self._parent_company

        if self.parent_company_id is None:
            return None

        loaded: Airline | None = self._run_loader("parent_company", self.parent_company_id)
        if loaded:
            self._parent_company = loaded

        return self._parent_company

    @parent_company.setter
    def parent_company(self, value: Airline | None) -> None:
        self._parent_company = value

        if value and getattr(value, 'id', None) is not None:
            self.parent_company_id = value.id
        else:
            self.parent_company_id = None

    @property
    def airplanes(self) -> list[Airplane]:
        if self._airplanes is not None:
            return self._airplanes

        if self.id is not None:
            loaded: list[Airplane] | None = self._run_loader("airplanes", self.id)
            if loaded is not None:
                self._airplanes = loaded
                return self._airplanes

        self._airplanes = []
        return self._airplanes

    @airplanes.setter
    def airplanes(self, value: list[Airplane]) -> None:
        self._airplanes = value

    @property
    def subcompanies(self) -> list[Airline]:
        if self._subcompanies is not None:
            return self._subcompanies

        if self.id is not None:
            loaded: list[Airline] | None = self._run_loader("subcompanies", self.id)
            if loaded is not None:
                self._subcompanies = loaded
                return self._subcompanies

        self._subcompanies = []
        return self._subcompanies

    @subcompanies.setter
    def subcompanies(self, value: list[Airline]) -> None:
        self._subcompanies = value

    @property
    def airline_staff(self) -> list[AirlineStaff]:
        if self._airline_staff is not None:
            return self._airline_staff

        if self.id is not None:
            loaded: list[AirlineStaff] | None = self._run_loader("airline_staff", self.id)
            if loaded is not None:
                self._airline_staff = loaded
                return self._airline_staff

        self._airline_staff = []
        return self._airline_staff

    @airline_staff.setter
    def airline_staff(self, value: list[AirlineStaff]) -> None:
        self._airline_staff = value

    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["parent_company_id"] = self._get_fk_value(self._parent_company, self.parent_company_id)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Airline:
        instance = cast(Airline, super().from_dict(data))

        cls._restore_fk(instance, data, "parent_company_id", "parent_company_id")

        return instance

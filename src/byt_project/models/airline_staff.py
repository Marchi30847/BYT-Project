from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .employee import Employee

if TYPE_CHECKING:
    from .airline import Airline


@dataclass(kw_only=True)
class AirlineStaff(Employee):
    MODEL_TYPE: ClassVar[str] = "airline_staff"

    airline_id: int | None = field(default=None, init=False)
    _airline: Airline | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        # airline_id — simple structural validation
        if self.airline_id is not None and not isinstance(self.airline_id, int):
            raise TypeError("airline_id must be an integer or None")

        # _airline — lazy-loaded value
        if self._airline is not None:
            if not isinstance(self._airline, Airline):
                raise TypeError("_airline must be an Airline instance or None")

    @property
    def airline(self) -> Airline | None:
        if self._airline is not None:
            return self._airline

        if self.airline_id is None:
            return None

        loaded: Airline | None = self._run_loader("airline", self.airline_id)
        if loaded:
            self._airline = loaded

        return self._airline

    @airline.setter
    def airline(self, value: Airline | None) -> None:
        self._airline = value

        if value and getattr(value, 'id', None) is not None:
            self.airline_id = value.id
        else:
            self.airline_id = None


    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["airline_id"] = self._get_fk_value(self._airline, self.airline_id)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AirlineStaff:
        instance = cast(AirlineStaff, super().from_dict(data))

        cls._restore_fk(instance, data, "airline_id", "airline_id")

        return instance

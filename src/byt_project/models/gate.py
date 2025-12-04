from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .flight import Flight
    from .terminal import Terminal


@dataclass(kw_only=True)
class Gate(BaseModel):
    MODEL_TYPE: ClassVar[str] = "gate"

    number: int
    is_open: bool = True

    terminal_id: int | None = field(default=None, init=False)
    terminal: Terminal | None = field(default=None)

    flight_ids: list[int] = field(default_factory=list, init=False)
    flights: list[Flight] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.terminal and getattr(self.terminal, 'id', None) is not None:
            self.terminal_id = self.terminal.id

        self.flight_ids = [f.id for f in self.flights if getattr(f, 'id', None) is not None]

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.terminal:
            data["terminal_id"] = self.terminal.id
        elif self.terminal_id is not None:
            data["terminal_id"] = self.terminal_id
        else:
            data["terminal_id"] = None

        f_ids: list[int] = [f.id for f in self.flights if f.id is not None]

        if not f_ids and self.flight_ids:
            f_ids = self.flight_ids

        data["flight_ids"] = f_ids

        data.pop("terminal", None)
        data.pop("flights", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Gate:
        instance = cast(Gate, super().from_dict(data))

        raw_terminal_id: str | int | None = data.get("terminal_id")
        instance.terminal_id = int(raw_terminal_id) if raw_terminal_id is not None else None

        raw_flight_ids: list[Any] = data.get("flight_ids")
        if isinstance(raw_flight_ids, list):
            instance.flight_ids = [int(x) for x in raw_flight_ids]

        return instance

    def add_flight(self, flight: Flight) -> None:
        if not self.is_open:
            raise ValueError(f"Gate {self.number} is closed. Cannot assign flight.")

        flight.gate = self
        self.flights.append(flight)

        if flight.id is not None:
            self.flight_ids.append(flight.id)

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False
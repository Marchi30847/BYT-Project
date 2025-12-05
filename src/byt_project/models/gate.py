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
    is_open: bool

    terminal_id: int | None = field(default=None, init=False)
    _terminal: Terminal | None = field(default=None, init=False, repr=False)

    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        # number
        if not isinstance(self.number, int) or self.number <= 0:
            raise ValueError("number must be a positive integer")

        # is_open
        if not isinstance(self.is_open, bool):
            raise TypeError("is_open must be a boolean")

        # terminal_id
        if self.terminal_id is not None and not isinstance(self.terminal_id, int):
            raise TypeError("terminal_id must be int or None")

        # _flights (lazy-loaded)
        if self._flights is not None and not isinstance(self._flights, list):
            raise TypeError("_flights must be a list or None")

    @property
    def terminal(self) -> Terminal | None:
        if self._terminal is not None:
            return self._terminal

        if self.terminal_id is None:
            return None

        loaded: Terminal | None = self._run_loader("terminal", self.terminal_id)
        if loaded:
            self._terminal = loaded

        return self._terminal

    @terminal.setter
    def terminal(self, value: Terminal | None) -> None:
        self._terminal = value
        if value and getattr(value, 'id', None) is not None:
            self.terminal_id = value.id
        else:
            self.terminal_id = None

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
        data: dict[str, Any] = super().to_dict()

        data["terminal_id"] = self._get_fk_value(self._terminal, self.terminal_id)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Gate:
        instance = cast(Gate, super().from_dict(data))

        cls._restore_fk(instance, data, "terminal_id", "terminal_id")

        return instance

    def add_flight(self, flight: Flight) -> None:
        if not self.is_open:
            raise ValueError(f"Gate {self.number} is closed. Cannot assign flight.")

        flight.gate = self

        if self._flights is not None:
            self._flights.append(flight)
        else:
            self._flights = [flight]

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

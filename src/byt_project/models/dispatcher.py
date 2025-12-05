from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .airline_staff import AirlineStaff

if TYPE_CHECKING:
    from .flight import Flight
    from .terminal import Terminal


@dataclass(kw_only=True)
class Dispatcher(AirlineStaff):
    MODEL_TYPE: ClassVar[str] = "dispatcher"

    specialization: str
    certification_level: int

    terminal_id: int | None = field(default=None, init=False)
    _terminal: Terminal | None = field(default=None, init=False, repr=False)

    _flights: list[Flight] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        # specialization
        if not isinstance(self.specialization, str) or not self.specialization.strip():
            raise ValueError("specialization must be a non-empty string")

        # certification_level
        if not isinstance(self.certification_level, int) or self.certification_level < 0:
            raise ValueError("certification_level must be a non-negative integer")


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
    def from_dict(cls, data: dict[str, Any]) -> Dispatcher:
        instance = cast(Dispatcher, super().from_dict(data))

        cls._restore_fk(instance, data, "terminal_id", "terminal_id")

        return instance

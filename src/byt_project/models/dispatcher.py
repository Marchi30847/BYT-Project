from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Any, TYPE_CHECKING, cast

from . import AirlineStaff

if TYPE_CHECKING:
    from .flight import Flight
    from .terminal import Terminal


@dataclass(kw_only=True)
class Dispatcher(AirlineStaff):
    MODEL_TYPE: ClassVar[str] = "dispatcher"

    specialization: str
    certification_level: int


    terminal_id: int | None = field(default=None, init=False)
    terminal: Terminal | None = field(default=None)

    flights: list[Flight] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.terminal and getattr(self.terminal, 'id', None) is not None:
            self.terminal_id = self.terminal.id

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        if self.terminal:
            data["terminal_id"] = self.terminal.id
        elif self.terminal_id is not None:
            data["terminal_id"] = self.terminal_id
        else:
            data["terminal_id"] = None

        data.pop("terminal", None)
        data.pop("flights", None)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Dispatcher:
        instance = cast(Dispatcher, super().from_dict(data))

        raw_airline_id: str | int | None = data.get("airline_id")
        instance.airline_id = int(raw_airline_id) if raw_airline_id is not None else None

        raw_terminal_id: str | int | None = data.get("terminal_id")
        instance.terminal_id = int(raw_terminal_id) if raw_terminal_id is not None else None

        return instance

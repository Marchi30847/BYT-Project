from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Any, TYPE_CHECKING, cast

from .base import BaseModel

if TYPE_CHECKING:
    from .gate import Gate
    from .dispatcher import Dispatcher
    from .security_officer import SecurityOfficer


class TerminalStatus(Enum):
    OPERATIONAL = "Operational"
    UNDER_MAINTENANCE = "Under Maintenance"
    CLOSED = "Closed"


@dataclass(kw_only=True)
class Terminal(BaseModel):
    MODEL_TYPE: ClassVar[str] = "terminal"

    number: str
    capacity: int
    status: TerminalStatus
    floors_count: int
    area: int

    _dispatchers: list[Dispatcher] | None = field(default=None, init=False, repr=False)

    _security_officers: list[SecurityOfficer] | None = field(default=None, init=False, repr=False)

    _gates: dict[int, Gate] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        # number (string ID of terminal e.g. "A", "B", "1")
        if not isinstance(self.number, str) or not self.number.strip():
            raise ValueError("Terminal.number must be a non-empty string")

        # capacity
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Terminal.capacity must be a positive integer")

        # status
        if not isinstance(self.status, TerminalStatus):
            raise TypeError("Terminal.status must be an instance of TerminalStatus enum")

        # floors_count
        if not isinstance(self.floors_count, int) or self.floors_count <= 0:
            raise ValueError("Terminal.floors_count must be a positive integer")

        # area (in m²)
        if not isinstance(self.area, int) or self.area <= 0:
            raise ValueError("Terminal.area must be a positive integer")

    @property
    def dispatchers(self) -> list[Dispatcher]:
        if self._dispatchers is not None:
            return self._dispatchers

        if self.id is not None:
            loaded: list[Dispatcher] | None = self._run_loader("dispatchers", self.id)
            if loaded is not None:
                self._dispatchers = loaded
                return self._dispatchers

        self._dispatchers = []
        return self._dispatchers

    @dispatchers.setter
    def dispatchers(self, value: list[Dispatcher]) -> None:
        self._dispatchers = value

    @property
    def security_officers(self) -> list[SecurityOfficer]:
        if self._security_officers is not None:
            return self._security_officers

        if self.id is not None:
            loaded: list[SecurityOfficer] | None = self._run_loader("security_officers", self.id)
            if loaded is not None:
                self._security_officers = loaded
                return self._security_officers

        self._security_officers = []
        return self._security_officers

    @security_officers.setter
    def security_officers(self, value: list[SecurityOfficer]) -> None:
        self._security_officers = value

    @property
    def gates(self) -> dict[int, Gate]:
        if self._gates is not None:
            return self._gates

        if self.id is not None:
            loaded_list: list[Gate] | None = self._run_loader("gates", self.id)
            if loaded_list is not None:
                self._gates = {g.number: g for g in loaded_list}
                return self._gates

        self._gates = {}
        return self._gates

    @gates.setter
    def gates(self, value: dict[int, Gate]) -> None:
        self._gates = value

    def __post_init__(self) -> None:
        super().__post_init__()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()

        data["status"] = self.status.value

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Terminal:
        data_copy: dict[str, Any] = dict(data)

        raw_status: Any = data_copy.get("status")
        if raw_status in {s.value for s in TerminalStatus}:
            data_copy["status"] = TerminalStatus(raw_status)
        else:
            # todo validate
            data_copy["status"] = None

        instance = cast(Terminal, super().from_dict(data_copy))

        return instance

    def add_gate(self, gate: Gate) -> None:
        if gate.number in self.gates:
            raise ValueError(f"Gate {gate.number} already exists in terminal {self.number}")

        gate.terminal = self

        self.gates[gate.number] = gate

    def get_gate(self, gate_number: int) -> Gate | None:
        return self.gates.get(gate_number)

    def list_gates(self) -> list[int]:
        return list(self.gates.keys())

    def open(self) -> None:
        self.status = TerminalStatus.OPERATIONAL

    def closed_for_maintenance(self) -> None:
        self.status = TerminalStatus.UNDER_MAINTENANCE

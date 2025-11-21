from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Dict, Optional, List

from .base import BaseModel
from .gate import Gate


class TerminalStatus(Enum):
    OPERATIONAL = "Operational"
    UNDER_MAINTENANCE = "Under Maintenance"
    CLOSED = "Closed"


@dataclass
class Terminal(BaseModel):
    MODEL_TYPE: ClassVar[str] = "terminal"

    terminal_number: str
    capacity: int
    status: TerminalStatus
    gates_count: int
    floors_count: int
    area: int
    gates: Dict[int, Gate] = field(default_factory=dict)

    def add_gate(self, gate: Gate) -> None:
        if gate.number in self.gates:
            raise ValueError(f"Gate {gate.number} already exists in terminal {self.terminal_number}")

        self.gates[gate.number] = gate

    def get_gate(self, gate_number: int) -> Optional[Gate]:
        return self.gates.get(gate_number)

    def list_gates(self) -> List[int]:
        return list(self.gates.keys())
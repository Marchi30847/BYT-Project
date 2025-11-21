from collections import defaultdict
from enum import Enum

from src.byt_project.models.gate import Gate


class TerminalStatus(Enum):
    OPERATIONAL = "Operational"
    UNDERMAINTENANCE = "Under Maintenance"
    CLOSED = "Closed"


class Terminal:
    def __init__(self, number: str, capacity: int, status: TerminalStatus, gatesCount: int, floorsCount: int, area: int):

        self.terminal_number = number
        self.capacity = capacity
        self.status = status
        self.gates_count = gatesCount
        self.floors_count = floorsCount
        self.area = area
        self.gates = dict()

    def add_gate(self, gate):
        if self.gates[gate.gate_number] is None:
            self.gates[gate.gate_number] = gate

    def get_gate(self, gate_number: str):
        for gate in self.gates:
            if gate.gate_number == gate_number:
                return gate
        return None

    def list_gates(self):
        return [g.gate_number for g in self.gates]
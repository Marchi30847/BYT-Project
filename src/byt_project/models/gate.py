from src.byt_project.models.terminal import Terminal


class Gate:
    def __init__(self, number: int, terminal: Terminal = None, is_open: bool = True):
        self.number = number
        self.isOpen = is_open
        self.terminal = terminal
        self.flights = []

    def addFlight(self, flight):
        if not self.isOpen:
            raise ValueError(f"Gate {self.number} is closed. Cannot assign flight.")

        flight.gate = self
        self.flights.append(flight)

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False
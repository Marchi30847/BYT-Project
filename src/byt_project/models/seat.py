class Seat:
    def __init__(self, number: int, row_letter: str):
        self.number = number
        self.row_letter = row_letter

        self.ticket = None

    def assign_ticket(self, ticket):
        if self.ticket is not None:
            raise ValueError("Seat already assigned to another ticket")
        self.ticket = ticket

    def is_available(self) -> bool:
        return self.ticket is None
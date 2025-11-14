class Ticket:
    def __init__(self, ticket_type: str, price: float, booking_date, luggage_limit: float):
        self.ticket_type = ticket_type
        self.price = price
        self.booking_date = booking_date
        self.luggage_limit = luggage_limit
        self.is_flagged = False

        self.seat = None

        self.bags = []

    def assign_seat(self, seat):
        if seat.ticket is not None:
            raise ValueError("This seat is already booked by another ticket")

        self.seat = seat
        seat.assign_ticket(self)

    def book(self):
        if self.seat is None:
            raise ValueError("Cannot book a ticket without selecting a seat first")
        return f"Ticket booked for seat {self.seat.row_letter}{self.seat.number}"
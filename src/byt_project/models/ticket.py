from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, List, Mapping, Any, Self, TYPE_CHECKING

from .base import BaseModel
from .flight import Flight

if TYPE_CHECKING:
    from .luggage import Luggage
    from .seat import Seat


@dataclass(kw_only=True)
class Ticket(BaseModel):
    MODEL_TYPE: ClassVar[str] = "ticket"

    type: str
    price: float
    booking_date: datetime
    luggage_limit: float
    seat: Seat
    luggage: List[Luggage]
    flight: Flight | None = None
    is_flagged: bool = False

    def assign_seat(self, seat: Seat) -> None:
        if seat.ticket is not None:
            raise ValueError("This seat is already booked by another ticket")

        self.seat = seat
        seat.assign_ticket(self)

    def assign_flight(self, flight: Flight) -> None:
        if not flight.book_seat(1):
            raise ValueError("No available seats for this flight")

        self.flight = flight

    def book(self) -> str:
        if self.seat is None:
            raise ValueError("Cannot book a ticket without selecting a seat first")

        return f"Ticket booked for seat {self.seat.row_letter}{self.seat.number}"

    @classmethod
    def from_dict(cls: type[Self], data: Mapping[str, Any]) -> Self:
        kwargs = dict(data)
        kwargs.pop("type", None)
        id_ = kwargs.pop("id", None)

        booking_date = datetime.fromisoformat(kwargs["booking_date"])

        obj = cls(
            type=str(kwargs["ticket_type"]),
            price=float(kwargs["price"]),
            booking_date=booking_date,
            luggage_limit=float(kwargs["luggage_limit"]),
        )
        obj.id = id_
        return obj

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["booking_date"] = self.booking_date.isoformat()
        return d
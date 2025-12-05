import pytest
from datetime import datetime
from src.byt_project.models.ticket import Ticket
from src.byt_project.models.seat import Seat
from src.byt_project.models.luggage import Luggage, SecurityStatus

#TODO НЕРАБОТАЕТ ИЗ-ЗА SEAT
def create_dummy_ticket(ticket_id=None):
    # Create Seat and Luggage with None ticket first to avoid circular dependency issues during init
    # We assume the models allow None temporarily or we bypass type checks at runtime
    seat = Seat(number=1, row_letter="A", ticket=None)
    luggage = Luggage(weight=20, dimensions="50x50x50", isFragile=False, securityStatus=SecurityStatus.NOT_FLAGGED,
                      ticket=None)

    ticket = Ticket(
        type="Economy",
        price=100.0,
        booking_date=datetime(2023, 10, 27, 10, 0),
        luggage_limit=23.0,
        seat=seat,
        luggage=[luggage]
    )
    if ticket_id:
        ticket.id = ticket_id

    # Link back
    seat.ticket = ticket
    luggage.ticket = ticket

    return ticket


def test_create_ticket(ticket_repository):
    ticket = create_dummy_ticket()
    created_ticket = ticket_repository.create(ticket)

    assert created_ticket.id is not None
    assert created_ticket.type == "Economy"
    assert created_ticket.price == 100.0
    # Check if seat and luggage are preserved (serialized/deserialized)
    # Note: BaseRepository uses to_dict/from_dict.
    # Ticket.to_dict/from_dict might not handle nested objects fully if not implemented in BaseModel
    # But let's verify what happens.


def test_find_ticket_by_id(ticket_repository):
    ticket = create_dummy_ticket()
    created = ticket_repository.create(ticket)

    found = ticket_repository.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.type == "Economy"


def test_update_ticket(ticket_repository):
    ticket = create_dummy_ticket()
    created = ticket_repository.create(ticket)

    created.price = 150.0
    updated = ticket_repository.update(created)

    assert updated is not None
    assert updated.price == 150.0

    found = ticket_repository.find_by_id(created.id)
    assert found.price == 150.0


def test_delete_ticket(ticket_repository):
    ticket = create_dummy_ticket()
    created = ticket_repository.create(ticket)

    assert ticket_repository.delete(created.id) is True
    assert ticket_repository.find_by_id(created.id) is None


def test_find_all_tickets(ticket_repository):
    ticket1 = create_dummy_ticket()
    ticket2 = create_dummy_ticket()
    # Modify ticket2 slightly to distinguish
    ticket2.type = "Business"
    ticket2.seat.number = 2

    ticket_repository.create(ticket1)
    ticket_repository.create(ticket2)

    all_tickets = ticket_repository.find_all()
    assert len(all_tickets) >= 2
    types = [t.type for t in all_tickets]
    assert "Economy" in types
    assert "Business" in types

import pytest
from datetime import datetime, date

from src.byt_project.models import Gate, Pilot, Shift
from src.byt_project.models.flight import Flight, FlightStatus
from src.byt_project.models.pilot import PilotRank


def test_create_flight(flight_repository):
    flight = Flight(flight_number="FL123", departure_time=datetime(2023, 10, 27, 10, 0))
    created_flight = flight_repository.create(flight)

    assert created_flight.id is not None
    assert created_flight.flight_number == "FL123"
    assert created_flight.status == FlightStatus.SCHEDULED


def test_find_flight_by_id(flight_repository):
    flight = Flight(flight_number="FL456", departure_time=datetime(2023, 10, 28, 12, 0))
    created = flight_repository.create(flight)

    found = flight_repository.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.flight_number == "FL456"


def test_update_flight(flight_repository):
    flight = Flight(flight_number="FL789", departure_time=datetime(2023, 10, 29, 14, 0))
    created = flight_repository.create(flight)

    created.status = FlightStatus.DELAYED
    updated = flight_repository.update(created)

    assert updated is not None
    assert updated.status == FlightStatus.DELAYED

    found = flight_repository.find_by_id(created.id)
    assert found.status == FlightStatus.DELAYED


def test_delete_flight(flight_repository):
    flight = Flight(flight_number="FL000", departure_time=datetime(2023, 10, 30, 16, 0))
    created = flight_repository.create(flight)

    assert flight_repository.delete(created.id) is True
    assert flight_repository.find_by_id(created.id) is None


def test_find_all_flights(flight_repository):
    flight1 = Flight(flight_number="FL111", departure_time=datetime(2023, 11, 1, 10, 0))
    flight2 = Flight(flight_number="FL222", departure_time=datetime(2023, 11, 2, 10, 0))
    flight_repository.create(flight1)
    flight_repository.create(flight2)

    all_flights = flight_repository.find_all()
    assert len(all_flights) >= 2
    numbers = [f.flight_number for f in all_flights]
    assert "FL111" in numbers
    assert "FL222" in numbers


def test_flight_associations(flight_repository, gate_repository, pilot_repository):
    # Setup repositories
    flight_repository.set_gate_repo(gate_repository)
    flight_repository.set_pilot_repo(pilot_repository)
    gate_repository.set_flight_repo(flight_repository)
    pilot_repository.set_flight_repo(flight_repository)

    # Create Gate
    gate = Gate(number=1, is_open=True)
    gate = gate_repository.create(gate)

    # Create Pilot
    pilot = Pilot(
        name="John", surname="Doe", dateOfBirth=datetime(2023, 10, 27, 10, 0), gender="M", nationality="United Kingdom", passportNumber="AB45OBA",
        hire_date=date(2020, 1, 1), salary=50000.0, shift=Shift.DAY,
        licence_number="P12345", rank=PilotRank.CAPTAIN, flight_hours=1000
    )
    pilot = pilot_repository.create(pilot)

    # Create Flight
    flight = Flight(flight_number="FL999", departure_time=datetime(2023, 12, 1, 10, 0))
    flight.gate = gate
    flight.assign_pilot(pilot)

    flight = flight_repository.create(flight)

    # Verify Flight -> Gate/Pilot
    loaded_flight = flight_repository.find_by_id(flight.id)
    assert loaded_flight is not None
    assert loaded_flight.gate.id == gate.id
    assert loaded_flight.gate.number == 1
    assert len(loaded_flight.pilots) == 1
    assert loaded_flight.pilots[0].id == pilot.id
    assert loaded_flight.pilots[0].licence_number == "P12345"

    # Verify Gate -> Flight
    loaded_gate = gate_repository.find_by_id(gate.id)
    assert loaded_gate is not None
    assert len(loaded_gate.flights) == 1
    assert loaded_gate.flights[0].id == flight.id

    # Verify Pilot -> Flight
    loaded_pilot = pilot_repository.find_by_id(pilot.id)
    assert loaded_pilot is not None
    assert len(loaded_pilot.flights) == 1
    assert loaded_pilot.flights[0].id == flight.id
import pytest
from src.byt_project.models.airline import Airline


def test_create_airline(airline_repository):
    airline = Airline(name="Test Airline", iata_code="TA", icao_code="TST", country="Testland")
    created_airline = airline_repository.create(airline)

    assert created_airline.id is not None
    assert created_airline.name == "Test Airline"
    assert created_airline.iata_code == "TA"
    assert created_airline.icao_code == "TST"
    assert created_airline.country == "Testland"


def test_find_airline_by_id(airline_repository):
    airline = Airline(name="Find Me", iata_code="FM", icao_code="FND", country="Findland")
    created = airline_repository.create(airline)

    found = airline_repository.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Find Me"


def test_update_airline(airline_repository):
    airline = Airline(name="Old Name", iata_code="ON", icao_code="OLD", country="Oldland")
    created = airline_repository.create(airline)

    created.name = "New Name"
    updated = airline_repository.update(created)

    assert updated is not None
    assert updated.name == "New Name"

    found = airline_repository.find_by_id(created.id)
    assert found.name == "New Name"


def test_delete_airline(airline_repository):
    airline = Airline(name="Delete Me", iata_code="DM", icao_code="DEL", country="Delland")
    created = airline_repository.create(airline)

    assert airline_repository.delete(created.id) is True
    assert airline_repository.find_by_id(created.id) is None


def test_find_all_airlines(airline_repository):
    airline1 = Airline(name="Airline 1", iata_code="A1", icao_code="AR1", country="Land1")
    airline2 = Airline(name="Airline 2", iata_code="A2", icao_code="AR2", country="Land2")
    airline_repository.create(airline1)
    airline_repository.create(airline2)

    all_airlines = airline_repository.find_all()
    assert len(all_airlines) >= 2
    names = [a.name for a in all_airlines]
    assert "Airline 1" in names
    assert "Airline 2" in names


def test_find_all_by_parent_id(airline_repository):
    parent = Airline(name="Parent", iata_code="PA", icao_code="PAR", country="Parentland")
    parent = airline_repository.create(parent)

    child1 = Airline(name="Child 1", iata_code="C1", icao_code="CH1", country="Childland")
    child1.parent_company = parent
    child2 = Airline(name="Child 2", iata_code="C2", icao_code="CH2", country="Childland")
    child2.parent_company = parent

    airline_repository.create(child1)
    airline_repository.create(child2)

    children = airline_repository.find_all_by_parent_id(parent.id)
    assert len(children) == 2
    child_names = [c.name for c in children]
    assert "Child 1" in child_names
    assert "Child 2" in child_names

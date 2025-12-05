import shutil
import pytest
from pathlib import Path

from src.byt_project.models import Pilot
from src.byt_project.repositories import GateRepository, PilotRepository
from src.byt_project.repositories.airline_repository import AirlineRepository
from src.byt_project.repositories.flight_repository import FlightRepository
from src.byt_project.repositories.customer_repository import CustomerRepository
from src.byt_project.repositories.ticket_repository import TicketRepository


@pytest.fixture
def airline_repository():
    return AirlineRepository()


@pytest.fixture
def flight_repository():
    return FlightRepository()

@pytest.fixture
def customer_repository():
    return CustomerRepository()

@pytest.fixture
def gate_repository():
    return GateRepository()

@pytest.fixture
def pilot_repository():
    return PilotRepository()

@pytest.fixture
def ticket_repository():
    return TicketRepository()

from datetime import date

import pytest
from src.byt_project.models.customer import Customer


def test_create_customer(customer_repository):
    customer = Customer(
    name="John",
    surname="Doe",
    dateOfBirth=date(1990, 1, 1),
    gender="M",
    nationality="USA",
    passportNumber="123456789",
    email="john@example.com",
    phone_number="123456789"
)
    created_customer = customer_repository.create(customer)

    assert created_customer.id is not None
    assert created_customer.name == "John"
    assert created_customer.email == "john@example.com"


def test_find_customer_by_id(customer_repository):
    customer = Customer(name="Jane", surname="Doe", email="jane@example.com", phone_number="987654321")
    created = customer_repository.create(customer)

    found = customer_repository.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Jane"


def test_update_customer(customer_repository):
    customer = Customer(name="Bob", surname="Smith", email="bob@example.com", phone_number="555555555")
    created = customer_repository.create(customer)

    created.email = "bob.new@example.com"
    updated = customer_repository.update(created)

    assert updated is not None
    assert updated.email == "bob.new@example.com"

    found = customer_repository.find_by_id(created.id)
    assert found.email == "bob.new@example.com"


def test_delete_customer(customer_repository):
    customer = Customer(name="Alice", surname="Wonder", email="alice@example.com", phone_number="111111111")
    created = customer_repository.create(customer)

    assert customer_repository.delete(created.id) is True
    assert customer_repository.find_by_id(created.id) is None

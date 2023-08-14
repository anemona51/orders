import json

import faker
import pytest
from starlette.testclient import TestClient

from main import app
from model.database import (
    clean_db,
    create_order_input,
    create_order_output,
    get_random_state,
)
from model.orders import OrderInput, State

fake = faker.Faker()


@pytest.fixture()
def client():
    client = TestClient(app)
    yield client


@pytest.fixture()
def one_order() -> str:
    stoks = fake.currency_code()
    quantity = fake.pyint()
    order_input = OrderInput(stoks=stoks, quantity=quantity)
    input_id = create_order_input(order_input)
    create_order_output(order_input, input_id, status=get_random_state())
    yield
    clean_db()


@pytest.fixture()
def orders_with_all_status() -> str:
    for status in State:
        stoks = fake.currency_code()
        quantity = fake.pyint()
        order_input = OrderInput(stoks=stoks, quantity=quantity)
        input_id = create_order_input(order_input)
        create_order_output(order_input, input_id, status=status.value)
    yield OrderInput(
        stoks=fake.currency_code(), quantity=fake.pyint()
    ).model_dump()
    clean_db()


@pytest.fixture()
def one_hundred_order_outputs() -> str:
    for _ in range(100):
        stoks = fake.currency_code()
        quantity = fake.pyint()
        order_input = OrderInput(stoks=stoks, quantity=quantity)
        input_id = create_order_input(order_input)
        create_order_output(order_input, input_id, status=get_random_state())
    yield OrderInput(
        stoks=fake.currency_code(), quantity=fake.pyint()
    ).model_dump()
    clean_db()


@pytest.fixture()
def wrong_order_input() -> str:
    return json.dumps({"stoks": fake.pyfloat(), "quantity": fake.text()})

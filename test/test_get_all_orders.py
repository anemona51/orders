from random import choice
from test.test_utils import assert_get_all_success, assert_status_success
from typing import Callable

import pytest

from model.assert_massages import AssertMessages
from model.database import (
    get_all_input_order,
    get_all_output_order,
    orders_input_collection,
)


@pytest.mark.priority_0
def test_get_all_output_order_when_no_input_order_exist_positive(
    client: Callable,
) -> None:
    expected_count = orders_input_collection.estimated_document_count()
    get_response = client.get(url=f"/orders")
    assert_status_success(get_response)
    assert (
        len(get_response.json()) == expected_count
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Output order")
    assert get_response.json() == [], AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(
        collection="Output order"
    )


@pytest.mark.priority_0
def test_get_all_output_order_positive(
    client: Callable, one_hundred_order_outputs: Callable
) -> None:
    input_orders = get_all_input_order()
    expected_count = orders_input_collection.estimated_document_count()
    get_response = client.get(url=f"/orders")
    assert_get_all_success(get_response, expected_count, input_orders)


@pytest.mark.priority_0
def test_get_all_output_order_after_creation_order_input_positive(
    client: Callable, orders_with_all_status: Callable
) -> None:
    expected_count = orders_input_collection.estimated_document_count() + 1
    client.post(url="/orders", json=orders_with_all_status)
    get_response = client.get(url=f"/orders")
    input_orders = get_all_input_order()
    assert_get_all_success(get_response, expected_count, input_orders)


@pytest.mark.priority_1
def test_get_all_output_order_after_get_order_input_positive(
    client: Callable, orders_with_all_status: Callable
) -> None:
    input_orders = get_all_input_order()
    expected_count = orders_input_collection.estimated_document_count()
    output_orders = choice(get_all_output_order())
    client.get(url=f"/orders/{output_orders['input_id']}")
    get_response = client.get(url=f"/orders")
    assert_get_all_success(get_response, expected_count, input_orders)

import json
import sys
from typing import Callable

import pytest

from const.messages import ErrorMessage
from model.assert_massages import AssertMessages
from model.database import (
    get_all_output_order,
    get_by_id_input_order,
    get_by_id_output_order,
    orders_input_collection,
    orders_output_collection,
)
from model.orders import State
from utils import get_input_order_id
from .conftest import fake

from .test_utils import assert_negative_response, assert_status_success


@pytest.mark.priority_0
def test_output_order_created_after_post_order_with_valid_data_positive(
    client: Callable,
    orders_with_all_status: Callable,
) -> None:
    previous_input_count = orders_input_collection.estimated_document_count()
    previous_output_count = orders_output_collection.estimated_document_count()
    previous_output_orders = get_all_output_order()
    response = client.post(url="/orders", json=orders_with_all_status)
    assert_status_success(response)
    new_order_input = get_by_id_input_order(get_input_order_id(response))
    order_id = str(new_order_input.pop("_id"))
    assert (
        new_order_input == orders_with_all_status
    ), AssertMessages.NOT_EQUAL_IN_DB.value.format(collection="Input order")
    assert (
        orders_input_collection.estimated_document_count() == previous_input_count + 1
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Input order")
    output_order = get_by_id_output_order(order_id)
    assert (
        output_order["status"] is not State.CANCELED
    ), AssertMessages.WRONG_STATE.value(state=output_order["status"])
    assert output_order["status"] in [
        State.PENDING.value,
        State.EXECUTED.value,
    ], AssertMessages.WRONG_STATE.value(state=output_order["status"])
    assert (
        orders_output_collection.estimated_document_count() == previous_output_count + 1
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Output order")
    for output_order in previous_output_orders:
        new_output_order = get_by_id_output_order(output_order["input_id"])
        assert (
            new_output_order == output_order
        ), AssertMessages.NOT_EQUAL_IN_DB.value.format(collection="Output order")


@pytest.mark.priority_0
def test_post_order_with_wrong_data_type_negative(
    client: Callable, wrong_order_input: Callable
) -> None:
    previous_object_count = orders_input_collection.estimated_document_count()
    response = client.post(url="/orders", json=wrong_order_input)
    assert_negative_response(
        response, wrong_order_input, ErrorMessage.WRONG_DATA, previous_object_count
    )


@pytest.mark.priority_0
def test_post_order_with_to_big_quantity_negative(
    client: Callable, orders_with_all_status: Callable
) -> None:
    previous_object_count = orders_input_collection.estimated_document_count()
    response = client.post(
        url="/orders", json={"stoks": fake.text(), "quantity": sys.float_info.max}
    )
    assert_negative_response(
        response, None, ErrorMessage.WRONG_QUANTITY_DATA, previous_object_count
    )
    response = client.post(
        url="/orders", json={"stoks": fake.text(), "quantity": -sys.float_info.max}
    )
    assert_negative_response(
        response, None, ErrorMessage.WRONG_QUANTITY_DATA, previous_object_count
    )


@pytest.mark.priority_1
@pytest.mark.parametrize(
    "body,message",
    [
        ({"stoks": ""}, ErrorMessage.NO_DATA),
        ({"quantity": 0}, ErrorMessage.NO_DATA),
        ({}, ErrorMessage.NO_DATA),
        ({"stoks": "", "quantity": 0}, ErrorMessage.WRONG_DATA),
        ({"jhgjgj": "njkhk", "quantity": "kkljl"}, ErrorMessage.WRONG_DATA),
    ],
)
def test_post_order_with_empty_fields_negative(
    client: Callable, orders_with_all_status: Callable, body, message
) -> None:
    previous_object_count = orders_input_collection.estimated_document_count()
    response = client.post(url="/orders", json=body)
    assert_negative_response(response, body, message, previous_object_count)


@pytest.mark.priority_1
def test_post_order_with_wrong_data_schema_negative(
    client: Callable, orders_with_all_status: Callable
) -> None:
    body = fake.pystr()
    previous_object_count = orders_input_collection.estimated_document_count()
    response = client.post(url="/orders", json=json.dumps(body))
    assert_negative_response(
        response, body, ErrorMessage.WRONG_DATA, previous_object_count
    )


@pytest.mark.priority_1
def test_post_order_with_no_data_negative(
    client: Callable, orders_with_all_status: Callable
) -> None:
    previous_object_count = orders_input_collection.estimated_document_count()
    response = client.post(url="/orders")
    assert_negative_response(
        response, None, ErrorMessage.NO_DATA, previous_object_count
    )

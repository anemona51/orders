from app.test.conftest import fake
from app.test.test_utils import assert_status_failed, assert_status_success
from typing import Callable

import pytest

from app.const.messages import ErrorMessage, SuccessMessage
from app.model.assert_massages import AssertMessages
from app.model.database import (
    get_all_output_order,
    get_by_id_output_order,
    orders_output_collection,
)
from app.utils import get_input_order_id, response_to_dict


@pytest.mark.priority_0
def test_getting_by_id_existed_output_orders_positive(
    client: Callable, orders_with_all_status: Callable
) -> None:
    previous_output_count = orders_output_collection.estimated_document_count()
    for output_orders in get_all_output_order():
        response = client.get(url=f"/orders/{output_orders['input_id']}")
        response_data = response_to_dict(response)
        success_message = response_data.pop("message")
        assert_status_success(response)
        output_order = get_by_id_output_order(output_orders["input_id"])
        output_order.pop("_id")
        assert (
            response_data == output_order
        ), AssertMessages.NOT_EQUAL_IN_DB.value.format(collection="Output order")
        assert (
            success_message == SuccessMessage.ORDER_WAS_FOUNDED.value
        ), AssertMessages.WRONG_MESSAGE.value
        assert (
            orders_output_collection.estimated_document_count() == previous_output_count
        ), AssertMessages.ITEM_WAS_CREATE_IN_DB.value.format(collection="Output order")


@pytest.mark.priority_0
def test_getting_by_id_output_order_after_creation_order_input_positive(
    client: Callable, orders_with_all_status: Callable
) -> None:
    previous_output_orders_count = orders_output_collection.estimated_document_count()
    previous_output_orders = get_all_output_order()
    post_response = client.post(url="/orders", json=orders_with_all_status)
    get_response = client.get(url=f"/orders/{get_input_order_id(post_response)}")
    response_data = response_to_dict(get_response)
    success_message = response_data.pop("message")
    assert_status_success(get_response)
    output_order = get_by_id_output_order(get_input_order_id(post_response))
    output_order.pop("_id")
    assert response_data == output_order, AssertMessages.NOT_EQUAL_IN_DB.value.format(
        collection="Output order"
    )
    assert (
        success_message == SuccessMessage.ORDER_WAS_FOUNDED.value
    ), AssertMessages.WRONG_MESSAGE.value
    assert (
        orders_output_collection.estimated_document_count()
        == previous_output_orders_count + 1
    ), AssertMessages.ITEM_WASNT_CREATE_IN_DB.value.format(collection="Output order")
    for output_order in previous_output_orders:
        new_output_order = get_by_id_output_order(output_order["input_id"])
        assert (
            new_output_order == output_order
        ), AssertMessages.NOT_EQUAL_IN_DB.value.format(collection="Output order")


@pytest.mark.priority_0
def test_getting_by_wrong_id_output_orders_negative(
    client: Callable, orders_with_all_status: Callable
) -> None:
    response = client.get(url=f"/orders/{fake.pystr()}")
    assert_status_failed(response, code=404, message=ErrorMessage.ORDER_NOT_FOUND.value)


@pytest.mark.priority_0
def test_getting_by_id_when_order_output_was_deleted_negative(
    client: Callable, one_order: Callable
) -> None:
    output_order = get_all_output_order()[0]
    orders_output_collection.delete_one({"input_id": output_order["input_id"]})
    response = client.get(url=f"/orders/{output_order['input_id']}")
    assert_status_failed(response, code=404, message=ErrorMessage.ORDER_NOT_FOUND.value)

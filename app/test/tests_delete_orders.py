from typing import Callable

import pytest

from app.const.messages import ErrorMessage, SuccessMessage
from app.model.assert_massages import AssertMessages
from app.model.database import (
    get_all_output_order,
    orders_output_collection,
    orders_input_collection,
    get_by_id_output_order,
)
from app.model.orders import State
from app.test.test_utils import (
    assert_status_failed,
    assert_status_success,
)
from app.utils import response_to_dict


@pytest.mark.priority_0
def test_delete_by_id_positive(
    client: Callable, one_hundred_order_outputs: Callable
) -> None:
    previous_input_count = orders_input_collection.estimated_document_count()
    previous_output_count = orders_output_collection.estimated_document_count()
    output_order = get_all_output_order()[0]
    delete_response = client.delete(url=f"/orders/{output_order['input_id']}")
    response_data = response_to_dict(delete_response)
    assert_status_success(delete_response)
    success_message = response_data.pop("message")
    output_order = get_by_id_output_order(output_order["input_id"])
    output_order.pop("_id")
    assert (
        response_data["status"] == State.CANCELED.value
    ), AssertMessages.WRONG_STATE.value(state=output_order["status"])
    assert response_data == output_order, AssertMessages.NOT_EQUAL_IN_DB.value.format(
        collection="Output order"
    )
    assert (
        success_message == SuccessMessage.ORDER_WAS_FOUNDED.value
    ), AssertMessages.WRONG_MESSAGE.value
    assert (
        orders_output_collection.estimated_document_count() == previous_output_count
    ), AssertMessages.ITEM_WAS_CREATE_IN_DB.value.format(collection="Output order")
    assert (
        orders_input_collection.estimated_document_count() == previous_input_count - 1
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Input order")


@pytest.mark.priority_0
def test_delete_by_id_when_order_output_in_cansel_status_negative(
    client: Callable, one_hundred_order_outputs: Callable
) -> None:
    previous_input_count = orders_input_collection.estimated_document_count()
    previous_output_count = orders_output_collection.estimated_document_count()
    output_order = next(
        output_order
        for output_order in get_all_output_order()
        if output_order["status"] == State.CANCELED.value
    )
    orders_output_collection.delete_one({"input_id": output_order["input_id"]})
    response = client.delete(url=f"/orders/{output_order['input_id']}")
    assert_status_failed(response, code=404, message=ErrorMessage.ORDER_NOT_FOUND.value)
    assert (
        orders_input_collection.estimated_document_count() == previous_input_count
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Input order")
    assert (
        orders_output_collection.estimated_document_count() == previous_output_count
    ), AssertMessages.ITEM_WAS_CREATE_IN_DB.value.format(collection="Output order")


@pytest.mark.priority_0
def test_delete_by_id_when_order_output_was_deleted_negative(
    client: Callable, one_order: Callable
) -> None:
    previous_input_count = orders_input_collection.estimated_document_count()
    previous_output_count = orders_output_collection.estimated_document_count()
    output_order = get_all_output_order()[0]
    orders_output_collection.delete_one({"input_id": output_order["input_id"]})
    response = client.delete(url=f"/orders/{output_order['input_id']}")
    assert_status_failed(response, code=404, message=ErrorMessage.ORDER_NOT_FOUND.value)
    assert (
        orders_input_collection.estimated_document_count() == previous_input_count
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Input order")
    assert (
        orders_output_collection.estimated_document_count() == previous_output_count
    ), AssertMessages.ITEM_WAS_CREATE_IN_DB.value.format(collection="Output order")

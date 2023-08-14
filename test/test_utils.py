from typing import List, Union

from httpx import Response

from const.messages import ErrorMessage
from model.assert_massages import AssertMessages
from model.database import orders_input_collection


def assert_status_failed(
    response, code: int = 400, message: Union[str, None] = None
) -> None:
    assert response.status_code == code
    if message:
        actual_message = response.json()["detail"]
        assert actual_message == message, AssertMessages.WRONG_MESSAGE.value


def assert_status_success(response: Response) -> None:
    assert response.status_code == 200


def assert_negative_response(
    response, body: Union[dict, None], message: ErrorMessage, previous_object_count: int
) -> None:
    assert_status_failed(response)
    assert response.read().decode() == message.value.format_map(
        {"response_data": body}
    ), AssertMessages.WRONG_MESSAGE
    assert (
        orders_input_collection.estimated_document_count() == previous_object_count
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value(collection="Input order")


def assert_get_all_success(
    get_response: Response, expected_count: int, input_orders: List = []
) -> None:
    assert_status_success(get_response)
    assert (
        len(get_response.json()) == expected_count
    ), AssertMessages.WRONG_NUMBER_OF_ITEMS.value.format(collection="Output order")
    [order.pop("_id") for order in input_orders]
    for input_order in get_response.json():
        assert input_order in input_orders, AssertMessages.NOT_EQUAL_IN_DB.value.format(
            collection="Output order"
        )

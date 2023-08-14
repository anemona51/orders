from enum import Enum


class SuccessMessage(Enum):
    ORDER_WAS_FOUNDED = "Order was founded"


class ErrorMessage(Enum):
    WRONG_DATA = "Error: Wrong data: {response_data}"
    NO_DATA = "Error: No data"
    ORDER_NOT_FOUND = "Error: Order not found"
    WRONG_QUANTITY_DATA = "Error: Number is too big/small"


map_errors = {
    "model_attributes_type": ErrorMessage.WRONG_DATA.value,
    "missing": ErrorMessage.NO_DATA.value,
    "int_parsing_size": ErrorMessage.WRONG_QUANTITY_DATA.value,
    "int_parsing": ErrorMessage.WRONG_DATA.value,
}

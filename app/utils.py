import json

from httpx import Response

from app.const.messages import SuccessMessage


def success_order_input_response(order_id: str) -> str:
    return json.dumps({"order_id": order_id})


def success_output_input_response(output_order: dict) -> str:
    output_order["message"] = SuccessMessage.ORDER_WAS_FOUNDED.value
    return json.dumps(output_order)


def response_to_dict(response: Response) -> str:
    return json.loads(response.json())


def get_input_order_id(response: Response) -> str:
    return json.loads(response.json())["order_id"]

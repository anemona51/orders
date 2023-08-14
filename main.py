from typing import Any, Dict, List, Union

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.background import BackgroundTasks
from starlette.responses import PlainTextResponse, Response

from const.messages import ErrorMessage, map_errors
from model.database import (
    create_order_input,
    create_order_output,
    delete_by_order_id,
    get_by_id_output_order,
    orders_input_collection,
    update_status,
)
from model.orders import OrderInput
from utils import success_order_input_response, success_output_input_response

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: List) -> Response:
    message = str(exc)
    for error in exc.errors():
        if error_type := error.get("type", None):
            message = map_errors.get(error_type).format_map(
                {"response_data": error.get("input", None)}
            )
    return PlainTextResponse(message, status_code=400)


@app.get("/orders")
async def get_all_orders() -> List[Dict[str, Any]]:
    result = []
    for order_input in orders_input_collection.find():
        order_input.pop("_id")
        result.append(order_input)
    return result


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> str:
    output_order = get_by_id_output_order(order_id)
    if output_order:
        output_order.pop("_id")
        return success_output_input_response(output_order)
    else:
        raise HTTPException(status_code=404, detail=ErrorMessage.ORDER_NOT_FOUND.value)


@app.post("/orders")
async def create_order(
    order: Union[OrderInput, None], background_tasks: BackgroundTasks
) -> str:
    order_id = create_order_input(order)
    if not order.stoks or order.quantity == 0:
        raise HTTPException(
            status_code=400,
            detail=ErrorMessage.WRONG_DATA.value.format(response_data=order),
        )
    background_tasks.add_task(update_status, order_id)
    create_order_output(order, order_id)
    return success_order_input_response(order_id)


@app.delete("/orders/{order_id}")
def delete_order(order_id: str) -> str:
    output_order = delete_by_order_id(order_id)
    if output_order:
        output_order.pop("_id")
        return success_output_input_response(output_order)
    else:
        raise HTTPException(status_code=404, detail=ErrorMessage.ORDER_NOT_FOUND.value)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

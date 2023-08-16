import random
import time
from typing import Union, List, Dict

from bson import ObjectId
from pymongo import MongoClient

from app.model.orders import OrderInput, OrderOutput, State

db_client = MongoClient("localhost", 27017)
orders_db = db_client["orders_database"]
orders_input_collection = orders_db["orders_input"]
orders_output_collection = orders_db["orders_output"]
errors = orders_db["errors"]


def get_all_state() -> List[str]:
    return [state.value for state in State]


def get_random_state() -> str:
    return random.choice(get_all_state())


def create_order_input(order: OrderInput) -> str:
    return str(orders_input_collection.insert_one(order.model_dump()).inserted_id)


def create_order_output(
    order: OrderInput, order_id: str, status: str = State.PENDING.value
) -> None:
    orders_output_collection.insert_one(
        OrderOutput(
            input_id=order_id,
            stoks=order.stoks,
            quantity=order.quantity,
            status=status,
        ).model_dump()
    )


def get_by_id_input_order(order_id: str) -> Dict[str, str]:
    return orders_input_collection.find_one(ObjectId(order_id))


def get_by_id_output_order(order_id: str) -> Dict[str, str]:
    return orders_output_collection.find_one({"input_id": order_id})


def get_not_equal_id_output_order(order_id: str) -> Dict[str, str]:
    return orders_output_collection.find_one({"input_id": {"$ne": order_id}})


def get_all_input_order() -> List[Dict[str, str]]:
    return [input_order for input_order in orders_input_collection.find()]


def get_all_output_order() -> List[Dict[str, str]]:
    return [output_order for output_order in orders_output_collection.find()]


def update_status(order_id: str, state: Union[str, None] = None) -> None:
    timeout = round(random.uniform(0.1, 1.0), 10)
    time.sleep(timeout)
    filter = {"input_id": order_id}
    new_status = {
        "$set": {"status": State.CANCELED.value if state else get_random_state()}
    }
    orders_output_collection.update_one(filter, new_status)
    return get_by_id_output_order(order_id)


def delete_by_order_id(order_id: str) -> Dict[str, str]:
    output_order = update_status(order_id, State.CANCELED)
    if output_order:
        orders_input_collection.delete_one({"_id": ObjectId(order_id)})
        return get_by_id_output_order(order_id)
    else:
        return output_order


def clean_db() -> None:
    orders_input_collection.delete_many({})
    orders_output_collection.delete_many({})

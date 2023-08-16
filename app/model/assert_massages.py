from enum import Enum


class AssertMessages(Enum):
    NOT_EQUAL_IN_DB = "{collection} in response doesn't equal {collection} in database"
    WRONG_MESSAGE = "Wrong message"
    ITEM_WASNT_CREATE_IN_DB = "{collection} item wasn't created"
    ITEM_WAS_CREATE_IN_DB = "{collection} item was created"
    WRONG_NUMBER_OF_ITEMS = "Wrong number of {collection} were returned"
    WRONG_STATE = "Output order in wrong state {state}"

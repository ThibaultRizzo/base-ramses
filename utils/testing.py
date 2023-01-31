from datetime import date, datetime, time
from enum import Enum
from functools import wraps
from http import HTTPStatus
import inspect
import json
from typing import Any, Callable, List, MutableMapping, Union
from uuid import UUID
from pandas import DataFrame
import numpy as np

def is_sub_class(instance: object, class_name: str, module_name: str = None):
    """
    Checks if instance inherit from a class matching class_name
    This is a light check as it does not
    """
    return class_name in [
        base_class.__name__
        for base_class in instance.__class__.__bases__
        if not module_name or base_class.__module__ == module_name
    ]


class BaseJSONEncoder(json.JSONEncoder):
    """
    Add support for custom types encoding
    """

    def default(self, o):
        """Default"""
        if o is None:
            return None
        if isinstance(o, (str, int, bytes, np.int64)):
            return int(o)
        if isinstance(o, (dict, list, DataFrame)):
            return o

        if o == Any:
            return "ANY_VALUE"
        if isinstance(o, (UUID, datetime, date, time)):
            return str(o)

        if isinstance(o, Enum):
            return o.value

        if hasattr(o, "dict"):
            return o.dict()

        if is_sub_class(o, "BaseModel", "sqlalchemy.orm.decl_api"):
            return o.dict()

        if inspect.isclass(o):
            return str(o)

        return json.JSONEncoder.default(self, o)


def serialize(obj):
    """Serializing method"""

    if obj == Any:
        return Any
    return BaseJSONEncoder().default(obj)


def assert_scalars(expected_item, received_item, *, preserve_types=False):
    """Assertion utility used in compare_item"""
    expected_str = serialize(expected_item)
    received_str = serialize(received_item)
    return (
        expected_str == Any
        or received_str == Any
        or (
            expected_str == received_str
            and (not preserve_types or get_type_or_none(expected_item) == get_type_or_none(received_item))
        )
    )

def get_type_or_none(obj):
    """Get type or none"""
    return type(obj) if obj is not None else ""

def get_key_or_none(obj: dict, key: str):
    """
    Get key of given dict else None if
      dict is not a dict
      dict does not have a value for this key
    """
    return obj.get(key, None) if isinstance(obj, dict) else None



def compare_item(expected_item: dict, received_item: dict, preserve_types=False):
    """
    Compares two dictionaries iterating on expected_item keys
    Settings preserved_types=True deactivatess stringification of compared outputs
    """

    if not isinstance(expected_item, dict):
        assert assert_scalars(
            expected_item, received_item, preserve_types=preserve_types
        ), f"""
        Expected {get_type_or_none(expected_item)} {expected_item}
        but received {get_type_or_none(received_item)} {received_item}
        """
    else:
        for key, expected in expected_item.items():
            received_item = serialize(received_item)
            received = get_key_or_none(received_item, key)

            if isinstance(received, list):
                compare_list(expected, received)
            elif isinstance(received, dict):
                compare_item(expected, received)
            else:
                assert assert_scalars(
                    expected, received, preserve_types=preserve_types
                ), f"""
            Expected {type(expected)} {expected} for field {key}
            but received {type(received)} {received}

            ___________
            
            Expected: {json.dumps(expected_item, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
            Received: {json.dumps(received_item, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
            """


def compare_scalar(expected_item, received_item):
    """
    Compares two variables if both are scalar types, else ignore
    """
    if isinstance(expected_item, (str, int, bytes)) and isinstance(received_item, (str, int, bytes)):
        assert (
            expected_item == received_item
        ), f"""
        Expected {type(expected_item) if expected_item is not None else ''} {expected_item}
        but received {type(received_item) if received_item is not None else ''} {received_item}
        """
        return True
    return False


def compare_list(expected_list, received_list):
    """
    Compares two list of dictionaries
    """
    assert len(received_list) == len(
        expected_list
    ), f"""
        Expected list of length {len(expected_list)} but received {len(received_list)}
        ____________


            Expected: {json.dumps(expected_list, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
            Received: {json.dumps(received_list, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
        
    """
    if len(expected_list) > 0:
        if isinstance(expected_list[0], (bool, str, int)):
            assert sorted(expected_list) == sorted(
                received_list
            ), f"""
                Expected list sorted in order at index {next((index for index,arr in enumerate([sorted(expected_list), sorted(received_list)]) if len(arr) > 2 and arr[0] != arr[1]), 0)}
                ____________


                    Expected: {json.dumps(expected_list, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
                    Received: {json.dumps(received_list, sort_keys=True, indent=4, cls=BaseJSONEncoder)}
                
            """
        else:
            for i, expected_item in enumerate(expected_list):
                received_item = received_list[i]
                compare_item(expected_item, received_item)


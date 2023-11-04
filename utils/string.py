"""
Module for generic string utilities
"""

import re

FIRST_CAP_REGEX = re.compile("(.)([A-Z][a-z]+)")
ALL_CAP_REGEX = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake_case(string: str):
    """
    Parse string from camel casing to snake casing
    Ex: MyLongString to my_long_string
    """
    interm_name = FIRST_CAP_REGEX.sub(r"\1_\2", string)
    return ALL_CAP_REGEX.sub(r"\1_\2", interm_name).lower()

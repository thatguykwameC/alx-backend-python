#!/usr/bin/env python3

"""
This function takes takes a string `k` and an int or float `v`
as arguments and returns a tuple.
"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple containing the string `k` and the square of the float `v`.

    Args:
        k (str): a string.
        v (Union[int, float]): an int or float.

    Returns:
        Tuple[str, float]: a tuple containing the string `k` and the square
        of the float `v`.
    """
    return (k, v ** 2)

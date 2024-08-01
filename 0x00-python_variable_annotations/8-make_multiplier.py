#!/usr/bin/env python3

"""
This function takes a float `multiplier` as argument and returns
a function that multiplies a float by `multiplier`
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a float by `multiplier`.

    Args:
        multiplier (float): the value to multiply by.

    Returns:
        Callable[[float], float]: a function that multiplies a float by
        `multiplier`.
    """
    def multiplier_fn(n: float) -> float:
        """
        Returns the product of `n` and `multiplier`.

        Args:
            n (float): the value to multiply.

        Returns:
            float: the product of `n` and `multiplier`.
        """
        return n * multiplier
    return multiplier_fn

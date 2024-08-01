#!/usr/bin/env python3

"""This function sums the elements of a list of floats."""

from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Sums the elements of a list of floats.

    Args:
        input_list (List[float]): A list of floats.

    Returns:
        float: The sum of the elements of the list.
    """
    return sum(input_list)

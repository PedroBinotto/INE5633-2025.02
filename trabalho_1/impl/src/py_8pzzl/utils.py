from pprint import pprint
from typing import Any, Callable, List
from collections import deque
from math import sqrt
import time
import sys

from py_8pzzl.types import Constraints, Params


def print_table(table: List[int], width: int = 5) -> None:
    cols = int(sqrt(len(table)))
    it = iter(table)
    matrix = [list(row) for row in zip(*[it] * cols)]

    for row in matrix:
        print(" ".join(f"{val:>{width}}" for val in row))


def live_update(f: Callable[[], Any], interval: float = 0.5) -> None:
    escape_code = "\033[H\033[J"
    sys.stdout.write(escape_code)
    f()
    time.sleep(interval)


def validate_input(input: Params) -> Constraints:
    sorted_input = list(input[1])
    sorted_input.sort()

    actual_data = tuple(sorted_input)
    expected_data = tuple(range(input[0] ** 2))

    if actual_data != expected_data:
        raise ValueError("Invalid input")

    solution = deque(expected_data)
    solution.rotate(-1)

    # 🔧 converter para tuple
    return (input, tuple(solution))


def capture_input() -> Constraints:
    data = list(map(int, sys.stdin.read().split()))  # <- força int
    it = iter(data)
    n = next(it)
    length = n * n
    table: List[int] = [None] * length
    for i in range(length):
        table[i] = next(it)

    return validate_input((n, tuple(table)))


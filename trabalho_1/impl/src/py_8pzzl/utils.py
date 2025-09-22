from pprint import pprint
from typing import Any, Callable
from collections import deque
from math import sqrt
import time
import sys

from py_8pzzl.algorithm import HFUNCTION_MAP
from py_8pzzl.types import Constraints, HFunctionLevel, Params, Path, State


def print_table(table: State, width: int = 5) -> None:
    cols = int(sqrt(len(table)))
    it = iter(table)
    matrix: list[list[int]] = [list(row) for row in zip(*[it] * cols)]

    print("\n")
    for row in matrix:
        print(" ".join(f"{val:>{width}}" for val in row))


def live_update(f: Callable[[], Any], interval: float = 0.5) -> None:
    escape_code = "\033[H\033[J"
    _ = sys.stdout.write(escape_code)
    f()
    time.sleep(interval)


def validate_input(input: Params) -> Constraints:
    sorted_input = list(input[1])
    sorted_input.sort()

    actual_data = tuple(sorted_input)
    expected_data = tuple(range(input[0] ** 2))

    if actual_data != expected_data:
        raise ValueError("Entrada inválida")

    solution = deque(expected_data)
    solution.rotate(-1)

    return (input, tuple(solution))


def print_result(path: Path) -> None:
    if path is not None:
        print("Path:\n")
        for idx, state in enumerate(path):
            print(f"{idx}:")
            print_table(state)
            print("\n***\n")
    else:
        print("Não há solução possível")


def capture_input() -> Constraints:
    data = list(map(str, sys.stdin.read().split()))
    it = iter(data)
    n = int(next(it))
    len = n * n
    table: list[int] = [-1] * len
    for i in range(len):
        table[i] = int(next(it))
    level = HFUNCTION_MAP[HFunctionLevel[next(it)]]

    return validate_input((n, tuple(table), level))

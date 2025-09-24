from datetime import datetime
from importlib import resources
import json
import pathlib
from typing import Any, Callable
from collections import deque
from math import sqrt
import time
import sys

from py_8pzzl.types import (
    NAME,
    NODE_MIN_SCORE,
    OUT_DIR,
    OUT_EXT,
    Constraints,
    HFunctionLevel,
    Memo,
    MemoizedState,
    OutputModel,
    Params,
    Path,
    Result,
    SetEncoder,
    State,
)


def get_project_root() -> pathlib.Path:
    root = resources.files(NAME)
    if isinstance(root, pathlib.Path):
        return root
    raise SystemError("Erro ao acessar sisema de arquivos")


def get_output_dir() -> pathlib.Path:
    return get_project_root().parent.parent / OUT_DIR


def get_output_file_name(s: State, l: HFunctionLevel) -> str:
    s_str = "".join(map(str, s))
    return f"{get_unix_timestamp()}_{s_str}_{l.name}.{OUT_EXT}"


def get_output_file(s: State, l: HFunctionLevel) -> pathlib.Path:
    return get_output_dir() / get_output_file_name(s, l)


def get_unix_time() -> float:
    return datetime.now().timestamp()


def get_unix_timestamp() -> str:
    return str(int(get_unix_time()))


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


def write_output(data: OutputModel, output_file: pathlib.Path) -> None:
    with open(output_file, "w") as f:
        json.dump(data, f, cls=SetEncoder)


def export_results(
    start_time: float,
    end_time: float,
    elapsed_time: float,
    h_level: HFunctionLevel,
    size: int,
    result: Result | None,
    output_file: pathlib.Path,
) -> None:
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output: OutputModel = {
        "start_time": start_time,
        "end_time": end_time,
        "elapsed_time": elapsed_time,
        "h_level": h_level,
        "size": size,
        "nodes_open": 0,
        "nodes_open_upper_bound": 0,
        "nodes_visited": 0,
        "path_size": 0,
        "path": None,
    }

    if result is not None:
        nodes_open = len(result["open"])
        nodes_open_upper_bound = result["open_upper_bound"]
        nodes_visited = len(result["visited"])
        path = result["path"]
        path_size = len(path) if path is not None else NODE_MIN_SCORE

        print("\nResultados:\n")
        print(f"Tamanho do caminho: {path_size}")
        print(f"Número de nós visitados: {nodes_visited}")
        print(f"Tamanho da fronteira (número de nós abertos): {nodes_open}")
        print(f"Tamanho máximo observado na fronteira: {nodes_open_upper_bound}")

        output["nodes_open"] = nodes_open
        output["nodes_open_upper_bound"] = nodes_open_upper_bound
        output["nodes_visited"] = nodes_visited
        output["path_size"] = path_size
        output["path"] = path
    else:
        print("Não há solução possível")

    print(f"Tempo descorrido (segundos): {elapsed_time}\n\n***")
    write_output(output, output_file)


def capture_input() -> Constraints:
    data = list(map(str, sys.stdin.read().split()))
    it = iter(data)
    n = int(next(it))
    len = n**2
    table: list[int] = [-1] * len
    for i in range(len):
        table[i] = int(next(it))
    level = HFunctionLevel[next(it)]

    return validate_input((n, tuple(table), level))


def initialize_memo(n: int) -> None:
    _ = Memo(n)


def use_memo(s: State) -> MemoizedState:
    try:
        return Memo().memoized(s)
    except Exception:
        raise ValueError("Tentativa de leitura sobre cache não inicializada")


def result(
    visited_nodes: set[State],
    open_nodes: set[State],
    open_nodes_upper_bound: int,
    path: Path | None,
) -> Result:
    return {
        "open": open_nodes,
        "open_upper_bound": open_nodes_upper_bound,
        "path": path,
        "visited": visited_nodes,
    }

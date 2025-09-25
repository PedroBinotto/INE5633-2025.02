from sys import exception
from py_8pzzl.algorithm import a_star
from py_8pzzl.heuristic import resolve
from py_8pzzl.types import Graph
from py_8pzzl.utils import (
    capture_input,
    export_results,
    get_output_file,
    get_unix_time,
    initialize_memo,
)


def run() -> None:
    constraints = capture_input()
    params = constraints[0]
    t = constraints[1]
    n = params[0]
    s = params[1]
    l = params[2]
    h = resolve(l)
    g = Graph(s)
    initialize_memo(n)

    try:
        start = get_unix_time()
        result = a_star(g, n, s, t, h)
        end = get_unix_time()

        elapsed = end - start
    except MemoryError as e:
        e.add_note("Não há solução possível")
        print(e)
        exit(0)

    export_results(start, end, elapsed, l, n, result, get_output_file(s, l))

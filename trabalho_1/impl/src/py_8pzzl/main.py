from datetime import datetime
import time
from py_8pzzl.algorithm import HFUNCTION_MAP, a_star
from py_8pzzl.types import Graph, Memo
from py_8pzzl.utils import (
    capture_input,
    export_results,
    get_output_file,
    get_unix_time,
)


def run() -> None:
    constraints = capture_input()
    params = constraints[0]
    t = constraints[1]
    n = params[0]
    s = params[1]
    l = params[2]
    h = HFUNCTION_MAP[l]
    g = Graph(s)
    _ = Memo(n)

    start = get_unix_time()
    result = a_star(g, n, s, t, h)
    end = get_unix_time()

    elapsed = end - start

    export_results(start, end, elapsed, l, n, result, get_output_file(s, l))

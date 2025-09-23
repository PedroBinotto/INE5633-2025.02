import time
from py_8pzzl.algorithm import HFUNCTION_MAP, a_star
from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input, print_result


def run() -> None:
    constraints = capture_input()
    params = constraints[0]
    t = constraints[1]
    n = params[0]
    s = params[1]
    l = params[2]
    g = Graph(s)

    start = time.time()
    result = a_star(g, n, s, t, l)
    end = time.time()

    elapsed = end - start

    print_result(result)
    print(f"Time elapsed (seconds): {elapsed}\n\n***")

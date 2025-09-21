import math
from py_8pzzl.algorithm import a_star
from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input, print_result, print_table


def run() -> None:
    params = capture_input()
    s = params[0][1]
    t = params[1]
    g = Graph(s)
    n = int(math.sqrt(len(s)))

    print_result(a_star(g, n, s, t, lambda x, y: 0))

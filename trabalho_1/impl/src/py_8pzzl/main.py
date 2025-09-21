import math
from py_8pzzl.algorithm import dfs
from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input, print_table


def run() -> None:
    params = capture_input()
    s = params[0][1]
    t = params[1]
    g = Graph(s)
    n = int(math.sqrt(len(s)))

    print("Solução:\n")
    print_table(t)

    dfs(g, n, s, t)
    return

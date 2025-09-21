import math
from py_8pzzl.algorithm import a_star
from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input, print_table


def run() -> None:
    params = capture_input()
    s = params[0][1]
    t = params[1]
    g = Graph(s)
    n = int(math.sqrt(len(s)))

    path = a_star(g, n, s, t, lambda x, y: 0)

    if path is not None:
        print("Path:\n")
        for idx, state in enumerate(path):
            print(f"{idx}:")
            print_table(state)
            print("\n***\n")
    else:
        print("Não há solução possível")

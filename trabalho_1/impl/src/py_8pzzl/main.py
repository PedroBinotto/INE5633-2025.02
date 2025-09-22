from pprint import pprint
from py_8pzzl.algorithm import HFUNCTION_MAP, a_star
from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input, print_result


def run() -> None:
    constraints = capture_input()
    params = constraints[0]
    n = params[0]
    s = params[1]
    l = params[2]
    t = constraints[1]
    g = Graph(s)

    print_result(a_star(g, n, s, t, HFUNCTION_MAP[l]))

if __name__ == "__main__":
    run()

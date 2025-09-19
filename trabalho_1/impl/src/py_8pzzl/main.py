from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input
from pprint import pprint


def a_star():
    pass


def run() -> None:
    params = capture_input()
    s = params[0][1]
    g = Graph(s)
    g.add_edge(s, (1, 2, 3, 4))
    g.add_edge(s, (5, 6, 7, 8))
    pprint(g.adj(s))
    return

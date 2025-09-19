from py_8pzzl.types import Graph
from py_8pzzl.utils import capture_input


def a_star():
    pass


def run() -> None:
    params = capture_input()
    s = params[0][1]
    g = Graph(s)
    g.add_edge(s, (1, 2, 3, 4))
    return

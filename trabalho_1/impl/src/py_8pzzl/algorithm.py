from typing import List

from py_8pzzl.types import UP, DOWN, LEFT, RIGHT, Graph, State
from py_8pzzl.utils import print_table


def compute_moves(s: State, k: int) -> List[State]:
    moves = []
    z = s.index(0)
    delta = {
        UP: -k,
        DOWN: k,
        LEFT: -1,
        RIGHT: 1,
    }
    n = int(k**2)
    u = z + delta[UP]
    d = z + delta[DOWN]
    l = z + delta[LEFT]
    r = z + delta[RIGHT]

    if z >= k:
        result = list(s)
        result[z], result[u] = result[u], result[z]
        moves.append(tuple(result))
    if z < n - k:
        result = list(s)
        result[z], result[d] = result[d], result[z]
        moves.append(tuple(result))
    if z % k != 0:
        result = list(s)
        result[z], result[l] = result[l], result[z]
        moves.append(tuple(result))
    if z % k != k - 1:
        result = list(s)
        result[z], result[r] = result[r], result[z]
        moves.append(tuple(result))

    return moves


def dfs(g: Graph, n: int, s: State, t: State) -> State:
    if s == t:
        return s
    for ss in compute_moves(s, n):
        g.add_edge(s, ss)
        return dfs(g, n, ss, t)


def a_star():
    pass

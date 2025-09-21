import heapq
from typing import Callable
from py_8pzzl.types import DOWN, LEFT, RIGHT, UP, Graph, Path, State


def compute_moves(s: State, k: int) -> list[State]:
    moves: list[State] = []
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


def a_star(
    g: Graph, n: int, s: State, t: State, h: Callable[[State, State], int]
) -> Path:
    """
    :param g: Targeted graph
    :type g: Graph

    :param n: Board size
    :type n: int

    :param s: Initial state
    :type s: State

    :param t: Targeted state
    :type t: State

    :param h: Heuristic function
    :type h: Callable[[State, State], int]

    :return: Path
    :rtype: Path
    """
    visited: set[State] = set()
    open = [(h(s, t), 0, s, [s])]

    while open:
        _, g_score, current, path = heapq.heappop(open)

        if current == t:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in compute_moves(current, n):
            g.add_edge(current, neighbor)
            if neighbor not in visited:
                g_next = g_score + 1
                f_next = g_next + h(neighbor, t)
                heapq.heappush(open, (f_next, g_next, neighbor, path + [neighbor]))

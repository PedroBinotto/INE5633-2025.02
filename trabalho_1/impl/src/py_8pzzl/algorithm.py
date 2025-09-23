import heapq
from typing import Callable
from py_8pzzl.types import (
    Direction,
    Graph,
    HFunctionLevel,
    HeuristicFunction,
    Path,
    Result,
    State,
)


def compute_moves(s: State, k: int) -> list[State]:
    delta_map: dict[Direction, Callable[[int, int], int]] = {
        Direction.UP: (lambda z, k: z + (-k)),
        Direction.DOWN: (lambda z, k: z + k),
        Direction.LEFT: (lambda z, k: z - 1),
        Direction.RIGHT: (lambda z, k: z + 1),
    }

    moves: list[State] = []
    z = s.index(0)
    n = int(k**2)

    u = delta_map[Direction.UP](z, k)
    d = delta_map[Direction.DOWN](z, k)
    l = delta_map[Direction.LEFT](z, k)
    r = delta_map[Direction.RIGHT](z, k)

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


def a_star(g: Graph, n: int, s: State, t: State, h: HeuristicFunction) -> Result | None:
    """
    'A*' search algorithm

    :param g: Targeted graph
    :type g: Graph

    :param n: Board size
    :type n: int

    :param s: Initial state
    :type s: State

    :param t: Targeted state
    :type t: State

    :param h: Heuristic function
    :type h: HeuristicFunction

    :return: Path
    :rtype: Path
    """
    visited: set[State] = set()
    open = [(h(s, t), 0, s, [s])]
    currently_open_count = len(open)
    open_upper_bound = currently_open_count

    while open:
        _, g_score, current, path = heapq.heappop(open)
        currently_open_count -= 1

        if current == t:
            currently_open = set(map(lambda x: x[2], open))
            return {
                "open": currently_open,
                "open_upper_bound": open_upper_bound,
                "path": path,
                "visited": visited,
            }

        if current in visited:
            continue
        visited.add(current)

        for neighbor in compute_moves(current, n):
            g.add_edge(current, neighbor)
            if neighbor not in visited:
                g_next = g_score + 1
                f_next = g_next + h(neighbor, t)
                currently_open_count += 1
                open_upper_bound = max(currently_open_count, open_upper_bound)

                heapq.heappush(open, (f_next, g_next, neighbor, path + [neighbor]))


def null_heuristic(_x: State, _y: State) -> int:
    return 0


def non_admissible_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    total = 0
    for i, v in enumerate(x):
        if v == 0:
            continue
        j = y.index(v)
        xi, yi = divmod(i, n)
        xj, yj = divmod(j, n)
        total += abs(xi - xj) + abs(yi - yj)
    return 2 * total


def manhattan_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    total = 0
    for i, v in enumerate(x):
        if v == 0:
            continue
        j = y.index(v)
        xi, yi = divmod(i, n)
        xj, yj = divmod(j, n)
        total += abs(xi - xj) + abs(yi - yj)
    return total


def custom_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    base = manhattan_heuristic(x, y)
    extra = 0
    for r in range(n):
        row = x[r * n : (r + 1) * n]
        for i in range(n):
            for j in range(i + 1, n):
                a, b = row[i], row[j]
                if a == 0 or b == 0:
                    continue
                ga, gb = y.index(a) // n, y.index(b) // n
                if ga == gb == r and y.index(a) > y.index(b):
                    extra += 2
    for c in range(n):
        col = [x[r * n + c] for r in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                a, b = col[i], col[j]
                if a == 0 or b == 0:
                    continue
                ga, gb = y.index(a) % n, y.index(b) % n
                if ga == gb == c and y.index(a) > y.index(b):
                    extra += 2
    return base + extra


HFUNCTION_MAP: dict[HFunctionLevel, HeuristicFunction] = {
    HFunctionLevel.L0: null_heuristic,
    HFunctionLevel.L1: non_admissible_heuristic,
    HFunctionLevel.L2: manhattan_heuristic,
    HFunctionLevel.L3: custom_heuristic,
}

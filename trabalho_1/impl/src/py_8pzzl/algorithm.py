from heapq import heappop as pq_pop, heappush as pq_push
from typing import Callable
from py_8pzzl.types import (
    NODE_MAX_SCORE,
    NODE_MIN_SCORE,
    Breadcrumb,
    Direction,
    Graph,
    HFunctionLevel,
    HeuristicFunction,
    Path,
    Result,
    State,
)
from py_8pzzl.utils import result, use_memo


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


def trace_path(breadcrumb: Breadcrumb, end: State) -> Path:
    path = [end]
    while end in breadcrumb:
        end = breadcrumb[end]
        path.append(end)
    path.reverse()
    return path


def a_star(
    g: Graph, n: int, s: State, t: State, h: HeuristicFunction, max_nodes: int = 400_000
) -> Result | None:
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

    :param max_nodes: Hard limit safeguard for explored nodes
    :type max_nodes: int

    :return: Result
    :rtype: Result | None
    """

    visited_nodes: set[State] = set()
    open_nodes: set[State] = {s}
    upper_bound = len(open_nodes)
    priority_queue: list[tuple[int, int, State]] = [(h(s, t, n), NODE_MIN_SCORE, s)]
    breadcrumb: Breadcrumb = {}
    gs: dict[State, int] = {s: NODE_MIN_SCORE}

    top_s: State = s
    top_h: int = h(s, t, n)

    while priority_queue:
        if len(visited_nodes) >= max_nodes:
            return result(
                visited_nodes,
                open_nodes,
                upper_bound,
                trace_path(breadcrumb, top_s),
            )

        curr_h, curr_g, curr_s = pq_pop(priority_queue)
        open_nodes.discard(curr_s)

        if curr_s == t:
            return result(
                visited_nodes,
                open_nodes,
                upper_bound,
                trace_path(breadcrumb, curr_s),
            )

        if curr_s in visited_nodes:
            continue
        visited_nodes.add(curr_s)

        if curr_h < top_h:
            top_h, top_s = curr_h, curr_s

        for move in compute_moves(curr_s, n):
            g.add_edge(curr_s, move)

            next_g = curr_g + 1

            if move in visited_nodes and next_g >= gs.get(move, NODE_MAX_SCORE):
                continue

            if next_g < gs.get(move, NODE_MAX_SCORE):
                breadcrumb[move] = curr_s
                gs[move] = next_g
                f_neighbor = next_g + h(move, t, n)
                pq_push(priority_queue, (f_neighbor, next_g, move))
                open_nodes.add(move)
                if len(open_nodes) > upper_bound:
                    upper_bound = len(open_nodes)

    return {
        "open": open_nodes,
        "open_upper_bound": upper_bound,
        "path": None,
        "visited": visited_nodes,
    }


def null_heuristic(_s: State, _t: State, _n: int) -> int:
    return NODE_MIN_SCORE


def non_admissible_heuristic(s: State, t: State, n: int) -> int:
    memo = use_memo(t)
    total = NODE_MIN_SCORE
    for idx, v in enumerate(s):
        if v == 0:
            continue
        x, y = divmod(idx, n)
        g_x, g_y = memo[v]
        total += abs(x - g_x) + abs(y - g_y)
    return 2 * total


def manhattan_heuristic(s: State, t: State, n: int) -> int:
    memo = use_memo(t)
    total = NODE_MIN_SCORE
    for idx, v in enumerate(s):
        if v == 0:
            continue
        x, y = divmod(idx, n)
        g_x, g_y = memo[v]
        total += abs(x - g_x) + abs(y - g_y)
    return total


def custom_heuristic(s: State, t: State, n: int) -> int:
    memo = use_memo(t)
    base = NODE_MIN_SCORE
    for idx, v in enumerate(s):
        if v == 0:
            continue
        x, y = divmod(idx, n)
        g_x, g_y = memo[v]
        base += abs(x - g_x) + abs(y - g_y)

    extra = NODE_MIN_SCORE

    for r in range(n):
        row = s[r * n : (r + 1) * n]
        idxs = [(i, v) for i, v in enumerate(row) if v != 0 and memo[v][0] == r]
        for idx in range(len(idxs)):
            for j in range(idx + 1, len(idxs)):
                vi = idxs[idx][1]
                vj = idxs[j][1]
                if memo[vi][1] > memo[vj][1]:
                    extra += 2
    for c in range(n):
        col = [s[r * n + c] for r in range(n)]
        idxs = [(i, v) for i, v in enumerate(col) if v != 0 and memo[v][1] == c]
        for idx in range(len(idxs)):
            for j in range(idx + 1, len(idxs)):
                vi = idxs[idx][1]
                vj = idxs[j][1]
                if memo[vi][0] > memo[vj][0]:
                    extra += 2

    return base + extra


HFUNCTION_MAP: dict[HFunctionLevel, HeuristicFunction] = {
    HFunctionLevel.L0: null_heuristic,
    HFunctionLevel.L1: non_admissible_heuristic,
    HFunctionLevel.L2: manhattan_heuristic,
    HFunctionLevel.L3: custom_heuristic,
}

import heapq
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


def reconstruct_path(breadcrumb: Breadcrumb, end: State) -> Path:
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

    :param max_nodes: Maximum number of nodes to visit before returning partial result
    :type max_nodes: int

    :return: Path
    :rtype: Path
    """

    visited_nodes: set[State] = set()
    open_nodes: set[State] = {s}
    open_nodes_upper_bound = len(open_nodes)
    gs: dict[State, int] = {s: NODE_MIN_SCORE}
    priority_queue: list[tuple[int, int, State]] = [(h(s, t, n), NODE_MIN_SCORE, s)]
    breadcrumb: Breadcrumb = {}

    best_state: State = s
    best_f: int = h(s, t, n)

    while priority_queue:
        if len(visited_nodes) >= max_nodes:
            return result(
                visited_nodes,
                open_nodes,
                open_nodes_upper_bound,
                reconstruct_path(breadcrumb, best_state),
            )

        f_current, g_current, current = heapq.heappop(priority_queue)
        open_nodes.discard(current)

        if current == t:
            return result(
                visited_nodes,
                open_nodes,
                open_nodes_upper_bound,
                reconstruct_path(breadcrumb, current),
            )

        if current in visited_nodes:
            continue
        visited_nodes.add(current)

        if f_current < best_f:
            best_f, best_state = f_current, current

        for neighbor in compute_moves(current, n):
            g.add_edge(current, neighbor)

            tentative_g = g_current + 1

            if neighbor in visited_nodes and tentative_g >= gs.get(
                neighbor, NODE_MAX_SCORE
            ):
                continue

            if tentative_g < gs.get(neighbor, NODE_MAX_SCORE):
                breadcrumb[neighbor] = current
                gs[neighbor] = tentative_g
                f_neighbor = tentative_g + h(neighbor, t, n)
                heapq.heappush(priority_queue, (f_neighbor, tentative_g, neighbor))
                open_nodes.add(neighbor)
                if len(open_nodes) > open_nodes_upper_bound:
                    open_nodes_upper_bound = len(open_nodes)

    return {
        "open": open_nodes,
        "open_upper_bound": open_nodes_upper_bound,
        "path": None,
        "visited": visited_nodes,
    }


def null_heuristic(_x: State, _y: State, _n: int) -> int:
    return NODE_MIN_SCORE


def non_admissible_heuristic(x: State, y: State, n: int) -> int:
    memo = use_memo(y, n)
    total = NODE_MIN_SCORE
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = memo[v]
        total += abs(xi - gx) + abs(yi - gy)
    return 2 * total


def manhattan_heuristic(x: State, y: State, n: int) -> int:
    memo = use_memo(y, n)
    total = NODE_MIN_SCORE
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = memo[v]
        total += abs(xi - gx) + abs(yi - gy)
    return total


def custom_heuristic(x: State, y: State, n: int) -> int:
    memo = use_memo(y, n)
    base = NODE_MIN_SCORE
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = memo[v]
        base += abs(xi - gx) + abs(yi - gy)

    extra = NODE_MIN_SCORE
    for r in range(n):
        row = x[r * n : (r + 1) * n]
        idxs = [(i, v) for i, v in enumerate(row) if v != 0 and memo[v][0] == r]
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                vi = idxs[i][1]
                vj = idxs[j][1]
                if memo[vi][1] > memo[vj][1]:
                    extra += 2
    for c in range(n):
        col = [x[r * n + c] for r in range(n)]
        idxs = [(i, v) for i, v in enumerate(col) if v != 0 and memo[v][1] == c]
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                vi = idxs[i][1]
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

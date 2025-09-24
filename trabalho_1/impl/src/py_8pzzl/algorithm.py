import heapq
import time
from typing import Callable
from py_8pzzl.types import (
    Direction,
    Graph,
    HFunctionLevel,
    HeuristicFunction,
    Result,
    State,
)


def compute_moves(s: State, k: int) -> list[State]:
    delta_map: dict[Direction, Callable[[int, int], int]] = {
        Direction.UP: (lambda z, k: z - k),
        Direction.DOWN: (lambda z, k: z + k),
        Direction.LEFT: (lambda z, k: z - 1),
        Direction.RIGHT: (lambda z, k: z + 1),
    }
    moves: list[State] = []
    z = s.index(0)
    n = k * k

    u = delta_map[Direction.UP](z, k)
    d = delta_map[Direction.DOWN](z, k)
    l = delta_map[Direction.LEFT](z, k)
    r = delta_map[Direction.RIGHT](z, k)

    if z >= k:
        r1 = list(s)
        r1[z], r1[u] = r1[u], r1[z]
        moves.append(tuple(r1))
    if z < n - k:
        r2 = list(s)
        r2[z], r2[d] = r2[d], r2[z]
        moves.append(tuple(r2))
    if z % k != 0:
        r3 = list(s)
        r3[z], r3[l] = r3[l], r3[z]
        moves.append(tuple(r3))
    if z % k != k - 1:
        r4 = list(s)
        r4[z], r4[r] = r4[r], r4[z]
        moves.append(tuple(r4))
    return moves


def a_star(
    g: Graph,
    n: int,
    s: State,
    t: State,
    h: HeuristicFunction,
    max_nodes: int = 400_000
) -> Result | None:
    start_time = time.time()

    open_heap: list[tuple[int, int, State]] = [(h(s, t), 0, s)]
    open_set: set[State] = {s}
    visited: set[State] = set()
    came_from: dict[State, State] = {}
    g_score: dict[State, int] = {s: 0}
    open_upper_bound = 1

    best_state: State = s
    best_f: int = h(s, t)

    def reconstruct_path(end: State) -> list[State]:
        path = [end]
        while end in came_from:
            end = came_from[end]
            path.append(end)
        path.reverse()
        return path

    while open_heap:
        if len(visited) >= max_nodes:
            path = reconstruct_path(best_state)
            elapsed = time.time() - start_time
            return {
                "open": set(open_set),
                "open_upper_bound": open_upper_bound,
                "path": path,
                "visited": visited,
                "partial": True,
                "depth": len(path) - 1,
                "elapsed_time": elapsed,
                "nodes_visited": len(visited),
            }

        f_current, g_current, current = heapq.heappop(open_heap)
        open_set.discard(current)

        if current == t:
            path = reconstruct_path(current)
            elapsed = time.time() - start_time
            return {
                "open": set(open_set),
                "open_upper_bound": open_upper_bound,
                "path": path,
                "visited": visited,
                "partial": False,
                "depth": len(path) - 1,
                "elapsed_time": elapsed,
                "nodes_visited": len(visited),
            }

        if current in visited:
            continue

        visited.add(current)

        if f_current < best_f:
            best_f = f_current
            best_state = current

        for neighbor in compute_moves(current, n):
            if g is not None:
                g.add_edge(current, neighbor)

            tentative_g = g_current + 1

            if neighbor in visited and tentative_g >= g_score.get(neighbor, 10**9):
                continue

            if tentative_g < g_score.get(neighbor, 10**9):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_neighbor = tentative_g + h(neighbor, t)
                heapq.heappush(open_heap, (f_neighbor, tentative_g, neighbor))
                open_set.add(neighbor)
                if len(open_set) > open_upper_bound:
                    open_upper_bound = len(open_set)

    elapsed = time.time() - start_time
    return {
        "open": set(open_set),
        "open_upper_bound": open_upper_bound,
        "path": None,
        "visited": visited,
        "partial": True,
        "depth": 0,
        "elapsed_time": elapsed,
        "nodes_visited": len(visited),
    }


_goal_pos_cache: dict[State, dict[int, tuple[int, int]]] = {}


def _goal_pos(y: State) -> dict[int, tuple[int, int]]:
    gp = _goal_pos_cache.get(y)
    if gp is None:
        n = int(len(y) ** 0.5)
        gp = {val: divmod(i, n) for i, val in enumerate(y)}
        _goal_pos_cache[y] = gp
    return gp


def null_heuristic(_x: State, _y: State) -> int:
    return 0


def non_admissible_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    gp = _goal_pos(y)
    s = 0
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = gp[v]
        s += abs(xi - gx) + abs(yi - gy)
    return 2 * s


def manhattan_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    gp = _goal_pos(y)
    s = 0
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = gp[v]
        s += abs(xi - gx) + abs(yi - gy)
    return s


def custom_heuristic(x: State, y: State) -> int:
    n = int(len(x) ** 0.5)
    gp = _goal_pos(y)
    base = 0
    for i, v in enumerate(x):
        if v == 0:
            continue
        xi, yi = divmod(i, n)
        gx, gy = gp[v]
        base += abs(xi - gx) + abs(yi - gy)

    extra = 0
    for r in range(n):
        row = x[r * n : (r + 1) * n]
        idxs = [(i, v) for i, v in enumerate(row) if v != 0 and gp[v][0] == r]
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                vi = idxs[i][1]
                vj = idxs[j][1]
                if gp[vi][1] > gp[vj][1]:
                    extra += 2
    for c in range(n):
        col = [x[r * n + c] for r in range(n)]
        idxs = [(i, v) for i, v in enumerate(col) if v != 0 and gp[v][1] == c]
        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                vi = idxs[i][1]
                vj = idxs[j][1]
                if gp[vi][0] > gp[vj][0]:
                    extra += 2

    return base + extra


HFUNCTION_MAP: dict[HFunctionLevel, HeuristicFunction] = {
    HFunctionLevel.L0: null_heuristic,
    HFunctionLevel.L1: non_admissible_heuristic,
    HFunctionLevel.L2: manhattan_heuristic,
    HFunctionLevel.L3: custom_heuristic,
}

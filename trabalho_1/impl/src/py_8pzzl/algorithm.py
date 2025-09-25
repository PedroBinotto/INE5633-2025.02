from heapq import heappop as pq_pop, heappush as pq_push
from typing import Callable
from py_8pzzl.types import (
    NODE_MAX_SCORE,
    NODE_MIN_SCORE,
    Breadcrumb,
    Direction,
    Graph,
    HeuristicFunction,
    Path,
    Result,
    State,
)
from py_8pzzl.utils import result


def compute_moves(s: State, k: int) -> list[State]:
    delta_map: dict[Direction, Callable[[int, int], int]] = {
        Direction.UP: (lambda z, k: z - k),
        Direction.DOWN: (lambda z, k: z + k),
        Direction.LEFT: (lambda z, k: z - 1),
        Direction.RIGHT: (lambda z, k: z + 1),
    }
    moves: list[State] = []
    z = s.index(0)
    n = int(k**2)
    u, d, l, r = z - k, z + k, z - 1, z + 1
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


def trace_path(breadcrumb: Breadcrumb, end: State) -> Path:
    path = [end]
    while end in breadcrumb:
        end = breadcrumb[end]
        path.append(end)
    path.reverse()
    return path


def a_star(g: Graph, n: int, s: State, t: State, h: HeuristicFunction, max_nodes: int = 400_000) -> Result | None:
    visited_nodes: set[State] = set()
    priority_queue: list[tuple[int, int, State]] = [(h(s, t, n), NODE_MIN_SCORE, s)]
    upper_bound = len(priority_queue)
    breadcrumb: Breadcrumb = {}
    gs: dict[State, int] = {s: NODE_MIN_SCORE}
    top_h: int = h(s, t, n)

    while priority_queue:
        curr_h, curr_g, curr_s = pq_pop(priority_queue)

        if curr_s == t:
            return result(
                len(visited_nodes),
                len(priority_queue),
                upper_bound,
                trace_path(breadcrumb, curr_s),
            )

        if max_nodes and len(visited_nodes) >= max_nodes:
            return result(
                len(visited_nodes),
                len(priority_queue),
                upper_bound,
                trace_path(breadcrumb, curr_s),
            )

        if curr_s in visited_nodes:
            continue
        visited_nodes.add(curr_s)

        if curr_h < top_h:
            top_h = curr_h

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
                if len(priority_queue) > upper_bound:
                    upper_bound = len(priority_queue)

    return result(len(visited_nodes), len(priority_queue), upper_bound, None)

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
    priority_queue: list[tuple[int, int, State]] = [(h(s, t, n), NODE_MIN_SCORE, s)]
    upper_bound = len(priority_queue)
    breadcrumb: Breadcrumb = {}
    gs: dict[State, int] = {s: NODE_MIN_SCORE}

    top_h: int = h(s, t, n)

    while priority_queue:
        if len(visited_nodes) >= max_nodes:
            raise MemoryError(
                f"Exploração do grafo ultrapassou limite de {max_nodes} nós. Interrompendo execução..."
            )

        curr_h, curr_g, curr_s = pq_pop(priority_queue)

        if curr_s == t:
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

from py_8pzzl.types import (
    NODE_MIN_SCORE,
    Coords,
    HFunctionLevel,
    HNamespace,
    HeuristicFunction,
    MemoizedState,
    State,
)
from py_8pzzl.utils import use_memo


def __ch_base_score(m: State, size: int, memo: MemoizedState) -> int:
    acc = NODE_MIN_SCORE
    for idx, v in enumerate(m):
        if v == 0:
            continue
        x, y = divmod(idx, size)
        g_x, g_y = memo[v]
        acc += abs(x - g_x) + abs(y - g_y)
    return acc


def __ch_extra_score(m: State, size: int, memo: MemoizedState):
    def h_search(m: State, i: int, j: int, memo: MemoizedState) -> list[Coords]:
        row = m[i * j : (i + 1) * j]
        idxs = [(idx, v) for idx, v in enumerate(row) if v != 0 and memo[v][0] == i]
        return idxs

    def v_search(m: State, i: int, j: int, memo: MemoizedState) -> list[Coords]:
        col = [m[r * j + i] for r in range(j)]
        idxs = [(idx, v) for idx, v in enumerate(col) if v != 0 and memo[v][1] == i]
        return idxs

    acc = NODE_MIN_SCORE

    for r in range(size):
        coords = h_search(m, r, size, memo)
        for idx in range(len(coords)):
            for jdx in range(idx + 1, len(coords)):
                vi = coords[idx][1]
                vj = coords[jdx][1]
                if memo[vi][1] > memo[vj][1]:
                    acc += 2

    for c in range(size):
        coords = v_search(m, c, size, memo)
        for idx in range(len(coords)):
            for jdx in range(idx + 1, len(coords)):
                vi = coords[idx][1]
                vj = coords[jdx][1]
                if memo[vi][0] > memo[vj][0]:
                    acc += 2
    return acc


def __null_heuristic(_s: State, _t: State, _n: int) -> int:
    return NODE_MIN_SCORE


def __non_admissible_heuristic(s: State, t: State, n: int) -> int:
    memo = use_memo(t)
    total = NODE_MIN_SCORE
    for idx, v in enumerate(s):
        if v == 0:
            continue
        x, y = divmod(idx, n)
        g_x, g_y = memo[v]
        total += abs(x - g_x) + abs(y - g_y)
    return 2 * total


def __manhattan_heuristic(s: State, t: State, n: int) -> int:
    memo = use_memo(t)
    total = NODE_MIN_SCORE
    for idx, v in enumerate(s):
        if v == 0:
            continue
        x, y = divmod(idx, n)
        g_x, g_y = memo[v]
        total += abs(x - g_x) + abs(y - g_y)
    return total


def __custom_heuristic(s: State, t: State, n: int) -> int:
    cache = use_memo(t)
    return __ch_base_score(s, n, cache) + __ch_extra_score(s, n, cache)


functions = HNamespace(
    l0=__null_heuristic,
    l1=__non_admissible_heuristic,
    l2=__manhattan_heuristic,
    l3=__custom_heuristic,
)


def resolve(l: HFunctionLevel) -> HeuristicFunction:
    return functions[l.name.lower()]  # pyright: ignore[reportGeneralTypeIssues]


__all__ = ["functions", "resolve"]

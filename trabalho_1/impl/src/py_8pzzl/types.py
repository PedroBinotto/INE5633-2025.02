from collections import defaultdict
from enum import Enum, auto
from typing import Callable

type State = tuple[int, ...]

type Params = tuple[int, State]
""" _N_(size), Initial state """

type Constraints = tuple[Params, State]
""" Params, Solution """

type Adj = defaultdict[State, list[State]]
""" Adjacency Matrix """

type Path = list[State] | None

type Heuristic = Callable[[State, State], int]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class HFunctionLevel(Enum):
    L0 = auto()
    L1 = auto()
    L2 = auto()
    L3 = auto()


DELTA_MAP: dict[Direction, Callable[[int, int], int]] = {
    Direction.UP: (lambda z, k: z + (-k)),
    Direction.DOWN: (lambda z, k: z + k),
    Direction.LEFT: (lambda z, k: z - 1),
    Direction.RIGHT: (lambda z, k: z + 1),
}

HFUNCTION_MAP: dict[HFunctionLevel, Heuristic] = {
    HFunctionLevel.L0: (lambda x, y: 0),
    HFunctionLevel.L1: (lambda x, y: 0),  # TODO
    HFunctionLevel.L2: (lambda x, y: 0),  # TODO
    HFunctionLevel.L3: (lambda x, y: 0),  # TODO
}


class Graph:
    def __init__(self, s: State) -> None:
        self.__adj: defaultdict[State, list[State]] = defaultdict()
        self.__adj[s] = []

    def add_edge(self, v: State, w: State) -> None:
        if w in self.__adj:
            return

        self.__adj[w] = []
        self.__adj[v].append(w)

    def v(self) -> list[State]:
        return list(self.__adj.keys())

    def adj(self, v: State) -> list[State]:
        return self.__adj[v]

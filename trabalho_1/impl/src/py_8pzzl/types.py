from collections import defaultdict
from enum import Enum, auto
from typing import Callable

type State = tuple[int, ...]
""" Tuple of size N ** 2, wherein N is the board size (edge) """

type Params = tuple[int, State, HeuristicFunction]
""" N (size), Initial state, Heuristic function """

type Constraints = tuple[Params, State]
""" Params, Solution """

type Adj = defaultdict[State, list[State]]
""" Adjacency Matrix """

type Path = list[State] | None

type HeuristicFunction = Callable[[State, State], int]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class HFunctionLevel(Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


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

from collections import defaultdict
from enum import Enum, auto, StrEnum
import json
from typing import Any, Callable, TypedDict

NAME = "py_8pzzl"
OUT_DIR = "output"
OUT_EXT = "json"

type State = tuple[int, ...]
""" Tuple of size N ** 2, wherein N is the board size (edge) """

type Params = tuple[int, State, HFunctionLevel]
""" N (size), Initial state, Heuristic function level """

type Constraints = tuple[Params, State]
""" Params, Solution """

type Adj = defaultdict[State, list[State]]
""" Adjacency Matrix """

type Path = list[State]

type HeuristicFunction = Callable[[State, State], int]


class HFunctionLevel(StrEnum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class Result(TypedDict):
    path: Path
    visited: set[State]
    open: set[State]
    open_upper_bound: int


class OutputModel(TypedDict):
    start_time: int
    end_time: int
    elapsed_time: int
    h_level: HFunctionLevel
    size: int
    path: Path | None
    path_size: int
    nodes_visited: int
    nodes_open: int
    nodes_open_upper_bound: int
    # TODO: adicionar nivel de dificuldade


class SetEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


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

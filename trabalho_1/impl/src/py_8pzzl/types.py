from collections import defaultdict
from typing import DefaultDict, List, Tuple
from pprint import pprint

type State = Tuple[int, ...]

type Params = Tuple[int, State]
""" _N_(size), Initial state """

type Constraints = Tuple[Params, State]
""" Params, Solution """

type Adj = DefaultDict[State, List[State]]
""" Adjacency Matrix """


class Graph:
    def __init__(self, s: State) -> None:
        self.__adj: DefaultDict[State, List[State]] = defaultdict()
        self.__adj[s] = []

    def add_edge(self, v: State, w: State) -> None:
        if w in self.__adj:
            raise KeyError("TODO: message")

        self.__adj[w] = []
        self.__adj[v] += w

        pprint(self.__adj)

from collections import defaultdict

UP = "UP"
DOWN = "DOWN"
RIGHT = "RIGHT"
LEFT = "LEFT"

type State = tuple[int, ...]

type Params = tuple[int, State]
""" _N_(size), Initial state """

type Constraints = tuple[Params, State]
""" Params, Solution """

type Adj = defaultdict[State, list[State]]
""" Adjacency Matrix """

type Path = list[State] | None


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

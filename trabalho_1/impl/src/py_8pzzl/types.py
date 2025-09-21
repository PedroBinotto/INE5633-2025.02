from collections import defaultdict
from typing import DefaultDict, List, Tuple, TypeAlias

# Definições de tipos
State: TypeAlias = Tuple[int, ...]             # Representa um estado (tupla de números)
Params: TypeAlias = Tuple[int, State]          # (N, estado_inicial)
Constraints: TypeAlias = Tuple[Params, State]  # (params, estado_objetivo)
Adj: TypeAlias = DefaultDict[State, List[State]]  # Matriz de adjacência


class Graph:
    def __init__(self, s: State) -> None:
        self.__adj: DefaultDict[State, List[State]] = defaultdict(list)
        self.__adj[s] = []

    def add_edge(self, v: State, w: State) -> None:
        if w in self.__adj:
            raise KeyError("Estado já existente na árvore de busca")

        self.__adj[w] = []
        self.__adj[v].append(w)

    def v(self) -> List[State]:
        return list(self.__adj.keys())

    def adj(self, v: State) -> List[State]:
        return self.__adj[v]

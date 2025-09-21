from collections import defaultdict
from typing import DefaultDict, List, Tuple, TypeAlias


State: TypeAlias = Tuple[int, ...]            
Params: TypeAlias = Tuple[int, State]         
Constraints: TypeAlias = Tuple[Params, State] 
Adj: TypeAlias = DefaultDict[State, List[State]]  


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

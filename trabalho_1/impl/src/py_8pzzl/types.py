from collections import defaultdict
from enum import Enum
from typing import Callable, TypedDict, Set

State = tuple[int,...]
HeuristicFunction = Callable[[State,State],int]
Path = list[State] | None

# só pra variar, ordem trocada dos enums
class Direcao(Enum):
    CIMA = 1
    BAIXO = 2
    ESQ = 3
    DIR = 4

class HFunctionLevel(Enum):
    L0="L0"; L1="L1"; L2="L2"; L3="L3"

class Grafo:
    def __init__(self, start: State):
        self._adj = defaultdict(list)
        self._adj[start] = []

    def add_edge(self, v: State, w: State):
        if w not in self._adj:
            self._adj[w]=[]
        if w not in self._adj[v]:
            self._adj[v].append(w)

    def vertices(self):
        return list(self._adj.keys())

    def vizinhos(self, v: State):
        return self._adj[v]

class Resultado(TypedDict, total=False):
    aberto: Set[State]
    limite_aberto: int
    path: Path
    visitados: Set[State]
    parcial: bool
    depth: int
    tempo: float
    nos: int

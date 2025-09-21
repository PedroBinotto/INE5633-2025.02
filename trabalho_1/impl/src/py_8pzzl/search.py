import heapq
from typing import Callable, Dict, List, Optional, Tuple
from py_8pzzl.types import State
from py_8pzzl.hashing import ZobristHasher


def a_star_search(
    start: State,
    goal: State,
    heuristic: Callable[[State, State], int],
    hasher: Optional[ZobristHasher] = None,
    max_nodes: int = 200_000,   # limite de segurança
    log_interval: int = 5000    # log a cada X expansões
) -> Tuple[Optional[List[State]], Dict[str, int]]:
    """
    Algoritmo A* genérico com monitoramento.
    Usa Zobrist Hashing se um `hasher` for fornecido.
    Retorna (caminho, estatísticas).
    """

    frontier: List[Tuple[int, int, State]] = []  # (f, g, state)
    heapq.heappush(frontier, (heuristic(start, goal), 0, start))

    # usa hash se tiver hasher
    start_key = hasher.hash_state(start) if hasher else start
    goal_key = hasher.hash_state(goal) if hasher else goal

    # came_from guarda: hash -> (estado, hash do pai)
    came_from: Dict[int, Tuple[State, Optional[int]]] = {start_key: (start, None)}
    g_score: Dict[int, int] = {start_key: 0}

    expanded = 0
    max_frontier = 1

    while frontier:
        f, g, current = heapq.heappop(frontier)
        expanded += 1
        max_frontier = max(max_frontier, len(frontier))

        # gera hash do estado atual
        current_key = hasher.hash_state(current) if hasher else current

        # logs periódicos para monitorar
        if expanded % log_interval == 0:
            print(f"[LOG] expandidos={expanded}, fronteira={len(frontier)}")

        # se atingir o limite, aborta
        if expanded >= max_nodes:
            print(f"[ABORTADO] limite de {max_nodes} nós atingido.")
            return None, {"expanded": expanded, "max_frontier": max_frontier}

        # checagem de objetivo
        if current_key == goal_key:
            return reconstruct_path(came_from, current_key), {
                "expanded": expanded,
                "max_frontier": max_frontier,
            }

        # gerar sucessores
        n = int(len(current) ** 0.5)
        zero_idx = current.index(0)
        x, y = divmod(zero_idx, n)

        moves = []
        if x > 0: moves.append((-1, 0))
        if x < n - 1: moves.append((1, 0))
        if y > 0: moves.append((0, -1))
        if y < n - 1: moves.append((0, 1))

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            new_idx = nx * n + ny
            new_state = list(current)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            new_state = tuple(new_state)

            new_key = hasher.hash_state(new_state) if hasher else new_state

            tentative_g = g + 1
            if new_key not in g_score or tentative_g < g_score[new_key]:
                g_score[new_key] = tentative_g
                f_score = tentative_g + heuristic(new_state, goal)
                heapq.heappush(frontier, (f_score, tentative_g, new_state))
                came_from[new_key] = (new_state, current_key)

    return None, {"expanded": expanded, "max_frontier": max_frontier}


def reconstruct_path(
    came_from: Dict[int, Tuple[State, Optional[int]]],
    current_key: int
) -> List[State]:
    """Reconstrói o caminho da solução a partir de came_from."""
    path: List[State] = []

    while current_key is not None:
        state, parent_key = came_from[current_key]
        path.append(state)
        current_key = parent_key

    path.reverse()
    return path

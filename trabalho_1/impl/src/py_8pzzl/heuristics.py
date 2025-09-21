from typing import Tuple
import math

State = Tuple[int, ...]

def uniform_cost(state: State, goal: State) -> int:
    """Custo uniforme = heurística zero"""
    return 0


def manhattan(state: State, goal: State) -> int:
    """Distância de Manhattan (admissível e simples)"""
    n = int(math.sqrt(len(state)))
    dist = 0
    for idx, value in enumerate(state):
        if value == 0:  # espaço vazio
            continue
        goal_idx = goal.index(value)
        x1, y1 = divmod(idx, n)
        x2, y2 = divmod(goal_idx, n)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist


def not_admissible(state: State, goal: State) -> int:
    """Heurística NÃO admissível (exemplo: Manhattan dobrado)"""
    return 2 * manhattan(state, goal)


def linear_conflict(state: State, goal: State) -> int:
    """
    Heurística mais forte: Manhattan + Linear Conflict
    Linear Conflict = duas peças corretas na mesma linha/coluna mas em ordem invertida
    """
    n = int(math.sqrt(len(state)))
    h = manhattan(state, goal)


    for row in range(n):
        row_vals = state[row * n:(row + 1) * n]
        for i in range(n):
            for j in range(i + 1, n):
                val_i, val_j = row_vals[i], row_vals[j]
                if val_i == 0 or val_j == 0:
                    continue
                goal_row_i, goal_col_i = divmod(goal.index(val_i), n)
                goal_row_j, goal_col_j = divmod(goal.index(val_j), n)
                if goal_row_i == row and goal_row_j == row and goal_col_i > goal_col_j:
                    h += 2

    
    for col in range(n):
        col_vals = [state[row * n + col] for row in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                val_i, val_j = col_vals[i], col_vals[j]
                if val_i == 0 or val_j == 0:
                    continue
                goal_row_i, goal_col_i = divmod(goal.index(val_i), n)
                goal_row_j, goal_col_j = divmod(goal.index(val_j), n)
                if goal_col_i == col and goal_col_j == col and goal_row_i > goal_row_j:
                    h += 2

    return h

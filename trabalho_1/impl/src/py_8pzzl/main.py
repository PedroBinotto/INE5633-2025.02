import time
from py_8pzzl.utils import capture_input, print_table
from py_8pzzl import heuristics as H
from py_8pzzl.search import a_star_search
from py_8pzzl.hashing import ZobristHasher


def run() -> None:
    params, goal = capture_input()
    n, start = params

    hasher = ZobristHasher(n)
    start_hash = hasher.hash_state(start)
    goal_hash = hasher.hash_state(goal)

    heuristics = {
        "uniforme": H.uniform_cost,
        "nao_admissivel": H.not_admissible,
        "manhattan": H.manhattan,
        "forte": H.linear_conflict,
    }

    print("Estado inicial:")
    print_table(start)
    print("\nObjetivo:")
    print_table(goal)
    print("\n")
    print("Estado inicial (tuple):", start)
    print("Objetivo (tuple):", goal)

    for nome, heur in heuristics.items():
        print("=" * 50)
        print(f"Rodando A* com heurística: {nome}")

        inicio = time.time()
        # agora passamos também o hasher
        path, stats = a_star_search(start, goal, heur, hasher)
        fim = time.time()

        if path is None:
            print("Sem solução encontrada.")
        else:
            print(f"Solução encontrada em {len(path)-1} movimentos")
            print(f"Tempo: {fim - inicio:.3f} segundos")
            print(f"Nós expandidos: {stats['expanded']}")
            print(f"Tamanho máximo da fronteira: {stats['max_frontier']}")
            print(f"Caminho reconstruído ({len(path)} estados):")
            for step in path:
                print_table(step)
                print()
        print("=" * 50 + "\n")


if __name__ == "__main__":
    run()

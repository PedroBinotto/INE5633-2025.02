import argparse
import time
from py_8pzzl.algorithm import a_star, HFUNCTION_MAP
from py_8pzzl.types import HFunctionLevel, State

State = tuple[int, ...]

# Objetivos
goal_15: State = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
)

goal_25: State = (
     1,  2,  3,  4,  5,
     6,  7,  8,  9, 10,
    11, 12, 13, 14, 15,
    16, 17, 18, 19, 20,
    21, 22, 23, 24,  0
)

# Casos 4×4
cases: dict[str, State] = {
    "Facil":   (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15),
    "Médio":   (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 12, 13, 14, 11, 15),
    "Medio":   (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 12, 13, 14, 11, 15),
    "Difícil": (5, 1, 2, 4, 9, 6, 3, 8, 13, 10, 7, 12, 0, 14, 11, 15),
    "Dificil": (5, 1, 2, 4, 9, 6, 3, 8, 13, 10, 7, 12, 0, 14, 11, 15),
}

# Casos 5×5
cases_5x5: dict[str, State] = {
    "Facil5": (
         1,  2,  3,  4,  5,
         6,  7,  8,  9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23,  0, 24
    ),
    "Medio5": (
         1,  2,  3,  4,  5,
         6,  7,  8,  9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22,  0, 23, 24
    ),
    "Dificil5": (
         6,  1,  2,  4,  5,
        11,  7,  3,  9, 10,
        16, 12,  8, 14, 15,
        21, 17, 13, 19, 20,
         0, 22, 18, 23, 24
    ),
}
cases.update(cases_5x5)

# Heurísticas
HMAP = {
    0: HFUNCTION_MAP[HFunctionLevel.L0],
    1: HFUNCTION_MAP[HFunctionLevel.L1],
    2: HFUNCTION_MAP[HFunctionLevel.L2],
    3: HFUNCTION_MAP[HFunctionLevel.L3],
}

# ===== Helpers =====
def render(state: State, k: int) -> str:
    return "\n".join(
        " ".join(f"{x:2d}" if x != 0 else " _" for x in state[i:i + k])
        for i in range(0, k * k, k)
    )

def print_path(path: list[State], k: int):
    print(f"\nPassos: {len(path) - 1}\n")
    for step, state in enumerate(path):
        print(f"Estado {step}")
        print(render(state, k))
        print()

def run_all_cases(k: int, h: int):
    hfun = HMAP[h]
    goal = goal_15 if k == 4 else goal_25

    print(f"\nResultados para k={k}, heurística L{h}\n")
    print(f"{'Caso':<12}{'Movimentos':<12}{'Nós Visitados':<15}{'Tempo (s)':<15}")
    print("-" * 65)

    for name, start in cases.items():
        if len(start) != k * k:
            continue
        t0 = time.perf_counter()
        res = a_star(None, k, start, goal, hfun)
        elapsed = time.perf_counter() - t0
        print(f"{name:<12}{res['depth']:<12}{res['nodes_visited']:<15}{elapsed:<15.7f}")

# ===== Programa principal =====
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=list(cases.keys()),
                    help="Escolha o caso para rodar (se omitido, roda todos)")
    ap.add_argument("--h", type=int, choices=[0, 1, 2, 3], default=2,
                    help="nível da heurística (L0..L3)")
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--debug", action="store_true",
                    help="imprime estado a estado o caminho ótimo")
    args = ap.parse_args()

    if args.case:
        start = cases[args.case]
        hfun = HMAP[args.h]
        goal = goal_15 if args.k == 4 else goal_25

        res = a_star(None, args.k, start, goal, hfun)
        print(f"Caso={args.case} | Heurística=L{args.h} | "
              f"Movimentos={res['depth']} | Nós Visitados={res['nodes_visited']}")

        if args.debug and res["path"]:
            print_path(res["path"], args.k)
    else:
        run_all_cases(args.k, args.h)

if __name__ == "__main__":
    main()

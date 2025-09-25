import sys
import argparse, time
from py_8pzzl.algorithm import a_star
from py_8pzzl.heuristic import resolve
from py_8pzzl.types import Graph, HFunctionLevel, State
from py_8pzzl.utils import (
    capture_input,
    export_results,
    get_output_file,
    get_unix_time,
    initialize_memo,
)

cases = {
    "Facil5": (
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 0, 24
    ),
    "Medio5": (
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 0, 23, 24
    ),
    "Dificil5": (
        6, 1, 2, 4, 5,
        11, 7, 3, 9, 10,
        16, 12, 8, 14, 15,
        21, 17, 13, 19, 20,
        0, 22, 18, 23, 24
    )
}

def run_case(name: str, s: State, n: int, h_level: HFunctionLevel):
    h = resolve(h_level)
    g = Graph(s)
    initialize_memo(n)
    start = get_unix_time()
    result = a_star(g, n, s, tuple(range(1, n*n)) + (0,), h)
    end = get_unix_time()
    elapsed = end - start
    export_results(start, end, elapsed, h_level, n, result, get_output_file(s, h_level))
    depth = len(result["path"]) - 1 if result["path"] else -1
    print(f"{name:<12}{depth:<12}{result['visited']:<15}{elapsed:<15.6f}")

def run_all(n: int, h_level: HFunctionLevel):
    print(f"\nResultados para k={n}, heurística {h_level.name}\n")
    print(f"{'Caso':<12}{'Movimentos':<12}{'Nós Visitados':<15}{'Tempo (s)':<15}")
    print("-" * 60)
    for name, s in cases.items():
        if len(s) != n * n:
            continue
        run_case(name, s, n, h_level)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=list(cases.keys()))
    ap.add_argument("--h", type=int, choices=[0, 1, 2, 3], default=2)
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()
    h_level = list(HFunctionLevel)[args.h]
    if args.case:
        run_case(args.case, cases[args.case], args.k, h_level)
    else:
        run_all(args.k, h_level)

if __name__ == "__main__":
    main()


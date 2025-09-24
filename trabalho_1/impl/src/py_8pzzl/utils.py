from collections import deque
from math import sqrt
import sys, time
from typing import Any, Callable

from py_8pzzl.types import Constraints, HFunctionLevel, Params, State


def print_tabuleiro(st: State, largura: int = 5):
    n = int(sqrt(len(st)))
    it = iter(st)
    linhas = [list(row) for row in zip(*[it] * n)]
    print()
    for linha in linhas:
        print(" ".join(f"{v:>{largura}}" for v in linha))


def live_refresh(f: Callable[[], Any], wait: float = 0.5):
    sys.stdout.write("\033[H\033[J")
    f()
    time.sleep(wait)


def validar_input(inp: Params) -> Constraints:
    dados = list(inp[1])
    dados.sort()
    esperado = tuple(range(inp[0] * inp[0]))
    if tuple(dados) != esperado:
        raise ValueError("entrada ruim")
    sol = deque(esperado)
    sol.rotate(-1)
    return (inp, tuple(sol))


def mostrar_res(res: dict | None):
    if not res:
        print("sem solução")
        return

    caminho = res.get("path")
    parc = res.get("partial", False)
    prof = res.get("depth", 0)

    if caminho:
        print("parcial" if parc else "ok", "em", prof, "movs\n")
        for i, st in enumerate(caminho):
            print(i, ":")
            print_tabuleiro(st)
            print()
    else:
        print("sem caminho")


def capturar_in() -> Constraints:
    dados = list(map(str, sys.stdin.read().split()))
    it = iter(dados)
    n = int(next(it))
    tot = n * n
    tbl = [-1] * tot
    for i in range(tot):
        tbl[i] = int(next(it))
    lvl = HFunctionLevel[next(it)]
    return validar_input((n, tuple(tbl), lvl))

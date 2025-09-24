import sys,time
from collections import deque
from math import sqrt
from typing import Any,Callable
from py_8pzzl.types import HFunctionLevel,State

def print_tab(st:State,w:int=5):
    n=int(sqrt(len(st)))
    it=iter(st)
    linhas=[list(r) for r in zip(*[it]*n)]
    print()
    for ln in linhas:
        print(" ".join(f"{v:>{w}}" for v in ln))

def refresh(fn:Callable[[],Any],espera:float=0.5):
    sys.stdout.write("\033[H\033[J")
    fn()
    time.sleep(espera)

def validar_input(inp):
    dados=list(inp[1]); dados.sort()
    esperado=tuple(range(inp[0]*inp[0]))
    if tuple(dados)!=esperado: 
        raise ValueError("entrada ruim")
    sol=deque(esperado); sol.rotate(-1)
    return (inp,tuple(sol))

def mostrar_res(res:dict|None):
    if not res: 
        print("sem solução"); return
    cam=res.get("path"); parc=res.get("parcial",False); prof=res.get("depth",0)
    if cam:
        print("parcial" if parc else "ok","em",prof,"movs\n")
        for i,st in enumerate(cam):
            print(i,":"); print_tab(st); print()
    else:
        print("sem caminho")

def capturar_in():
    dados=list(map(str,sys.stdin.read().split()))
    it=iter(dados); n=int(next(it))
    tam=n*n; tbl=[0]*tam
    for i in range(tam): tbl[i]=int(next(it))
    lvl=HFunctionLevel[next(it)]
    return validar_input((n,tuple(tbl),lvl))

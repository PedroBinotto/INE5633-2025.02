import argparse,time
from py_8pzzl.algorithm import a_star,HFUNCTION_MAP
from py_8pzzl.types import HFunctionLevel,State
from py_8pzzl import utils

goal4:State=(1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,0)
goal5:State=(1,2,3,4,5, 6,7,8,9,10, 11,12,13,14,15,
             16,17,18,19,20, 21,22,23,24,0)

cases={
  "Facil":(1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15),
  "Medio":(1,2,3,4,5,6,7,8,9,10,0,12,13,14,11,15),
  "Dificil":(5,1,2,4,9,6,3,8,13,10,7,12,0,14,11,15),
  "Facil5":(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            16,17,18,19,20,21,22,23,0,24),
  "Medio5":(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            16,17,18,19,20,21,22,0,23,24),
  "Dificil5":(6,1,2,4,5,11,7,3,9,10,16,12,8,14,15,
              21,17,13,19,20,0,22,18,23,24)
}

HMAP={
  0:HFUNCTION_MAP[HFunctionLevel.L0],
  1:HFUNCTION_MAP[HFunctionLevel.L1],
  2:HFUNCTION_MAP[HFunctionLevel.L2],
  3:HFUNCTION_MAP[HFunctionLevel.L3]
}

def run_all(k:int,h:int):
    goal=goal4 if k==4 else goal5
    print("\nrodando k=",k," h=",h,"\n")
    print(f"{'Caso':<10}{'Movs':<8}{'Visit':<10}{'Tempo':<10}")
    print("-"*40)
    for nome,start in cases.items():
        if len(start)!=k*k: continue
        t0=time.perf_counter()
        r=a_star(None,k,start,goal,HMAP[h])
        t=time.perf_counter()-t0
        print(f"{nome:<10}{r['depth']:<8}{r['nos']:<10}{t:<10.6f}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--case",choices=list(cases.keys()))
    ap.add_argument("--h",type=int,choices=[0,1,2,3],default=2)
    ap.add_argument("--k",type=int,default=4)
    ap.add_argument("--debug",action="store_true")
    args=ap.parse_args()

    if args.case:
        start=cases[args.case]
        goal=goal4 if args.k==4 else goal5
        r=a_star(None,args.k,start,goal,HMAP[args.h])
        print("caso",args.case,"h",args.h,"movs",r["depth"],"visit",r["nos"])
        if args.debug and r["path"]:
            for st in r["path"]:
                utils.print_tab(st)
                print()
    else:
        run_all(args.k,args.h)

if __name__=="__main__": main()

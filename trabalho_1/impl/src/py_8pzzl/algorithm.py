import heapq, time
from py_8pzzl.types import Direcao as Direction, Grafo as Graph
from py_8pzzl.types import HFunctionLevel, HeuristicFunction, Resultado as Result, State

def moves(s:State,k:int)->list[State]:
    delta={
        Direction.CIMA:  lambda z,k: z-k,
        Direction.BAIXO: lambda z,k: z+k,
        Direction.ESQ:   lambda z,k: z-1,
        Direction.DIR:   lambda z,k: z+1,
    }
    z=s.index(0); n=k*k; out=[]
    u,d,l,r=z-k,z+k,z-1,z+1
    if z>=k: 
        r1=list(s); r1[z],r1[u]=r1[u],r1[z]; out.append(tuple(r1))
    if z<n-k: 
        r2=list(s); r2[z],r2[d]=r2[d],r2[z]; out.append(tuple(r2))
    if z%k!=0: 
        r3=list(s); r3[z],r3[l]=r3[l],r3[z]; out.append(tuple(r3))
    if z%k!=k-1: 
        r4=list(s); r4[z],r4[r]=r4[r],r4[z]; out.append(tuple(r4))
    return out

def a_star(g:Graph,n:int,start:State,goal:State,h:HeuristicFunction,max_nodes:int=400000)->Result|None:
    ini=time.time()
    open_heap=[(h(start,goal),0,start)]
    open_set={start}; visited=set(); came_from={}; gscore={start:0}
    max_open=1; melhor=start; melhor_f=h(start,goal)

    def path(end):
        p=[end]
        while end in came_from: end=came_from[end]; p.append(end)
        return list(reversed(p))

    while open_heap:
        if len(visited)>=max_nodes:
            return {"path":path(melhor),"visited":visited,"parcial":True,
                    "depth":len(path(melhor))-1,"tempo":time.time()-ini,
                    "nos":len(visited)}
        f_atual,g_atual,cur=heapq.heappop(open_heap); open_set.discard(cur)
        if cur==goal:
            return {"path":path(cur),"visited":visited,"parcial":False,
                    "depth":len(path(cur))-1,"tempo":time.time()-ini,
                    "nos":len(visited)}
        if cur in visited: continue
        visited.add(cur)
        if f_atual<melhor_f: melhor_f=f_atual; melhor=cur
        for viz in moves(cur,n):
            if g: g.add_edge(cur,viz)
            tent_g=g_atual+1
            if viz in visited and tent_g>=gscore.get(viz,10**9): continue
            if tent_g<gscore.get(viz,10**9):
                came_from[viz]=cur; gscore[viz]=tent_g
                fviz=tent_g+h(viz,goal)
                heapq.heappush(open_heap,(fviz,tent_g,viz))
                open_set.add(viz)
                if len(open_set)>max_open: max_open=len(open_set)

    return {"path":None,"visited":visited,"parcial":True,"depth":0,
            "tempo":time.time()-ini,"nos":len(visited)}

_goal_cache={}
def _gpos(y:State):
    if y not in _goal_cache:
        n=int(len(y)**0.5); _gpos_map={v:divmod(i,n) for i,v in enumerate(y)}
        _goal_cache[y]=_gpos_map
    return _goal_cache[y]

def h0(_x:State,_y:State)->int: return 0

def h1(x:State,y:State)->int:
    n=int(len(x)**0.5); gp=_gpos(y); s=0
    for i,v in enumerate(x):
        if v==0: continue
        xi,yi=divmod(i,n); gx,gy=gp[v]; s+=abs(xi-gx)+abs(yi-gy)
    return 2*s

def h2(x:State,y:State)->int:
    n=int(len(x)**0.5); gp=_gpos(y); s=0
    for i,v in enumerate(x):
        if v==0: continue
        xi,yi=divmod(i,n); gx,gy=gp[v]; s+=abs(xi-gx)+abs(yi-gy)
    return s

def h3(x:State,y:State)->int:
    n=int(len(x)**0.5); gp=_gpos(y); base=0
    for i,v in enumerate(x):
        if v==0: continue
        xi,yi=divmod(i,n); gx,gy=gp[v]; base+=abs(xi-gx)+abs(yi-gy)
    extra=0
    for r in range(n):
        row=x[r*n:(r+1)*n]; idxs=[(i,v) for i,v in enumerate(row) if v!=0 and gp[v][0]==r]
        for i in range(len(idxs)):
            for j in range(i+1,len(idxs)):
                vi,vj=idxs[i][1],idxs[j][1]
                if gp[vi][1]>gp[vj][1]: extra+=2
    for c in range(n):
        col=[x[r*n+c] for r in range(n)]; idxs=[(i,v) for i,v in enumerate(col) if v!=0 and gp[v][1]==c]
        for i in range(len(idxs)):
            for j in range(i+1,len(idxs)):
                vi,vj=idxs[i][1],idxs[j][1]
                if gp[vi][0]>gp[vj][0]: extra+=2
    return base+extra

HFUNCTION_MAP={
    HFunctionLevel.L0:h0,
    HFunctionLevel.L1:h1,
    HFunctionLevel.L2:h2,
    HFunctionLevel.L3:h3
}

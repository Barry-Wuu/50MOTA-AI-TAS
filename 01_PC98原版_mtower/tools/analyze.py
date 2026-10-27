"""层内分析：把门/怪视为可通行，算"到达目标最少需要哪几把钥匙"，并列出各区连通性。"""
import collections
import mota_core as M

def door_at(f,x,y):
    o=M.obj_raw(f,x,y)
    if o and M.TYPE.get(M.oatr(o,3))=='DOOR':
        return M.DOOR_OF.get(o), o
    return None, None

def analyze(f, targets):
    """targets: list of (label,(x,y))。返回每个 target 所需的门集合（最少钥匙链）。"""
    # BFS over states (cell, frozenset(doors opened)) where opening a door costs its color
    # we want min number of yellow/blue/red needed
    from collections import deque
    start=(None,None)
    # 起点由调用者通过 targets 里的 'start' 指定
    return None

def regions(f, start):
    """返回 忽略门/怪 的连通区划分，以及每区包含的门颜色统计。"""
    seen=set(); regs=[]
    for c in [(x,y) for y in range(13) for x in range(13) if M.terrain(f,x,y)!=1]:
        if c in seen: continue
        q=collections.deque([c]); comp={c}; seen.add(c)
        while q:
            x,y=q.popleft()
            for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
                nx,ny=x+dx,y+dy
                if 0<=nx<13 and 0<=ny<13 and M.terrain(f,nx,ny)!=1 and (nx,ny) not in comp:
                    comp.add((nx,ny)); seen.add((nx,ny)); q.append((nx,ny))
        regs.append(comp)
    return regs

if __name__=='__main__':
    import sys
    f=int(sys.argv[1]); sx=int(sys.argv[2]); sy=int(sys.argv[3])
    regs=regions(f,(sx,sy))
    print(f"{f}F 忽略门/怪 连通区数={len(regs)}")
    for i,comp in enumerate(sorted(regs,key=len,reverse=True)):
        cols=collections.Counter()
        for c in comp:
            col,_=door_at(f,*c)
            if col: cols[col]+=1
        stairs=[f"({c[0]},{c[1]})->{M.WARP.get((f,c[0],c[1]))}" for c in comp if M.terrain(f,*c)==2]
        print(f"  区{i}: {len(comp)}格 门{ dict(cols) } 梯{stairs}")

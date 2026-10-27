# -*- coding: utf-8 -*-
import mota_core as M, collections
w = M.World.new()
def passable(f,x,y):
    t = w.terrain_at(f,x,y)
    return t != 1
for f in range(6,12):
    # BFS over terrain, doors & monsters both passable
    seen={}; regs=[]
    for y0 in range(1,12):
        for x0 in range(1,12):
            if not passable(f,x0,y0) or (x0,y0) in seen: continue
            rid=len(regs); q=collections.deque([(x0,y0)]); seen[(x0,y0)]=rid; cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 1<=nx<=11 and 1<=ny<=11 and passable(f,nx,ny) and (nx,ny) not in seen:
                        seen[(nx,ny)]=rid; q.append((nx,ny))
            regs.append(cells)
    print("="*70); print("FLOOR %d  区域数=%d"%(f,len(regs)))
    for i,cells in enumerate(regs):
        tags=[]
        for (x,y) in sorted(cells):
            o=w.at(f,x,y); t=w.terrain_at(f,x,y)
            if t==2: tags.append("梯(%d,%d)"%(x,y))
            if o:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='KEY': tags.append("钥%s(%d,%d)"%({'y':'黄','b':'蓝','r':'红'}[M.KEY_OF[o]],x,y))
                elif ty=='DOOR': tags.append(("暗墙" if o==89 else "门%s"%{'y':'黄','b':'蓝','r':'红'}[M.DOOR_OF[o]])+"(%d,%d)"%(x,y))
                elif ty in ('SELL','BUY'): tags.append("商店(%d,%d)"%(x,y))
                elif ty=='MONSTER':
                    hp,atk,dfn,g=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)
                    tags.append("怪%d(%d,%d)hp%d"%(o,x,y,hp))
        print("  区%d (%d格): %s"%(i,len(cells),' '.join(tags)))

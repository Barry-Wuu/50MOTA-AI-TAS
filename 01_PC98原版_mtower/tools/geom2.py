# -*- coding: utf-8 -*-
import mota_core as M, collections
w = M.World.new()
def blk(f,x,y):
    o=w.at(f,x,y)
    if not o: return False
    ty=M.TYPE.get(M.oatr(o,3),'?')
    if ty in ('DOOR','MONSTER'): return True
    return False
for f in range(6,12):
    seen={}; regs=[]
    for y0 in range(1,12):
        for x0 in range(1,12):
            if w.terrain_at(f,x0,y0)==1 or blk(f,x0,y0) or (x0,y0) in seen: continue
            rid=len(regs); q=collections.deque([(x0,y0)]); seen[(x0,y0)]=rid; cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 1<=nx<=11 and 1<=ny<=11 and w.terrain_at(f,nx,ny)!=1 and not blk(f,nx,ny) and (nx,ny) not in seen:
                        seen[(nx,ny)]=rid; q.append((nx,ny))
            regs.append(cells)
    print("="*72); print("FLOOR %d  真实区域数=%d (门/怪视为墙)"%(f,len(regs)))
    for i,cells in enumerate(regs):
        tags=[]
        for (x,y) in sorted(cells):
            o=w.at(f,x,y); t=w.terrain_at(f,x,y)
            if t==2: tags.append("梯(%d,%d)"%(x,y))
            if o:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='KEY': tags.append("钥%s(%d,%d)"%({'y':'黄','b':'蓝','r':'红'}[M.KEY_OF[o]],x,y))
                elif ty in ('SELL','BUY'): tags.append("商店(%d,%d)"%(x,y))
                elif ty=='STATUS':
                    hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                    tags.append("物(%d,%d)%s"%(x,y,('hp%d'%hp if hp else ('atk%d'%atk if atk else 'def%d'%dfn))))
        # 统计该区四周的阻挡物
        around=collections.Counter()
        for (x,y) in cells:
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=x+dx,y+dy
                if not(1<=nx<=11 and 1<=ny<=11): continue
                o=w.at(f,nx,ny)
                if not o:
                    if w.terrain_at(f,nx,ny)==1: around['墙']+=1
                    continue
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='DOOR':
                    around['门' if o!=89 else '暗墙']+=1
                elif ty=='MONSTER':
                    hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                    around['怪%d(hp%d)'%(o,hp)]+=1
        print("  区%d (%2d格) 邻:%s | %s"%(i,len(cells),dict(around),' '.join(tags)))

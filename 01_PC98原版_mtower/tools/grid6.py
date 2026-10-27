# -*- coding: utf-8 -*-
import mota_core as M, collections
w = M.World.new()
def blocker(f,x,y):
    o=w.at(f,x,y)
    if not o: return None
    ty=M.TYPE.get(M.oatr(o,3),'?')
    if ty=='DOOR': return '暗' if o==89 else {'y':'黄','b':'蓝','r':'红'}[M.DOOR_OF[o]]
    if ty=='MONSTER':
        hp,atk,dfn,g=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)
        return '%d:%d/%d/%d'%(o,hp,atk,dfn)
    return None
for f in range(6,12):
    # region ids
    seen={}; rid={}; regs=[]
    for y0 in range(1,12):
        for x0 in range(1,12):
            if w.terrain_at(f,x0,y0)==1 or blocker(f,x0,y0) or (x0,y0) in seen: continue
            r=len(regs); q=collections.deque([(x0,y0)]); seen[(x0,y0)]=r; cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 1<=nx<=11 and 1<=ny<=11 and w.terrain_at(f,nx,ny)!=1 and not blocker(f,nx,ny) and (nx,ny) not in seen:
                        seen[(nx,ny)]=r; q.append((nx,ny))
            regs.append(cells); rid.update({c:r for c in cells})
    print("="*90); print("FLOOR %d  区数=%d"%(f,len(regs)))
    print("     "+"".join("%-9s"%("x=%d"%x) for x in range(1,12)))
    for y in range(1,12):
        row=[]
        for x in range(1,12):
            t=w.terrain_at(f,x,y); o=w.at(f,x,y); b=blocker(f,x,y)
            if t==1: row.append("  墙")
            elif b: row.append("  "+b)
            else:
                tags=[]
                if t==2: tags.append("梯")
                if o:
                    ty=M.TYPE.get(M.oatr(o,3),'?')
                    if ty=='KEY': tags.append("K"+{'y':'黄','b':'蓝','r':'红'}[M.KEY_OF[o]])
                    elif ty in ('SELL','BUY'): tags.append("店")
                    elif ty=='STATUS':
                        hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                        nm=M.oname(o)
                        tags.append(("血+%d"%hp) if hp else ("攻+%d"%atk) if atk else ("防+%d"%dfn) if dfn else nm[:4])
                    elif ty=='ITEM': tags.append("物"+str(o))
                    else: tags.append(str(o))
                r=rid.get((x,y),'-')
                row.append(("R%-2d"%r)+("".join(tags) if tags else "  .  "))
        print("y=%-3d"%y+"".join("%-9s"%c for c in row))

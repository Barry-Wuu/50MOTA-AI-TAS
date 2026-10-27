# -*- coding: utf-8 -*-
import mota_core as M, collections
w = M.World.new()
def blocker(f,x,y):
    o=w.at(f,x,y)
    if not o: return None
    ty=M.TYPE.get(M.oatr(o,3),'?')
    if ty=='DOOR': return '暗墙' if o==89 else '门'+{'y':'黄','b':'蓝','r':'红'}[M.DOOR_OF[o]]
    if ty=='MONSTER':
        hp,atk,dfn,g=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12),M.oatr(o,13)
        return '怪%d(hp%d,atk%d,def%d,g%d)'%(o,hp,atk,dfn,g)
    return None
for f in range(6,12):
    seen={}; regs=[]
    for y0 in range(1,12):
        for x0 in range(1,12):
            if w.terrain_at(f,x0,y0)==1 or blocker(f,x0,y0) or (x0,y0) in seen: continue
            rid=len(regs); q=collections.deque([(x0,y0)]); seen[(x0,y0)]=rid; cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 1<=nx<=11 and 1<=ny<=11 and w.terrain_at(f,nx,ny)!=1 and not blocker(f,nx,ny) and (nx,ny) not in seen:
                        seen[(nx,ny)]=rid; q.append((nx,ny))
            regs.append(cells)
    print("="*74); print("FLOOR %d"%f)
    for i,cells in enumerate(regs):
        cs=sorted(cells)
        tags=[]
        for (x,y) in cs:
            o=w.at(f,x,y); t=w.terrain_at(f,x,y)
            if t==2: tags.append("梯(%d,%d)"%(x,y))
            if o:
                ty=M.TYPE.get(M.oatr(o,3),'?')
                if ty=='KEY': tags.append("钥%s(%d,%d)"%({'y':'黄','b':'蓝','r':'红'}[M.KEY_OF[o]],x,y))
                elif ty in ('SELL','BUY'): tags.append("商店(%d,%d)"%(x,y))
                elif ty=='STATUS':
                    hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                    tags.append("物(%d,%d)%s"%(x,y,M.oname(o)[:6] if hp else ('atk+1' if atk else ('def+1' if dfn else '铁盾'))))
        bset=collections.Counter()
        for (x,y) in cs:
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=x+dx,y+dy
                if not(1<=nx<=11 and 1<=ny<=11): continue
                b=blocker(f,nx,ny)
                if b: bset[b]+=1
        print(" 区%-2d 格%-40s 界:%s"%(i,','.join("%d,%d"%(x,y) for x,y in cs),' | '.join('%s×%d'%(k,v) for k,v in sorted(bset.items()))))
        if tags: print("      物: "+' '.join(tags))

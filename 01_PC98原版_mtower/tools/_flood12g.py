import mota_core as M, run_segs as R
from collections import deque
w=M.World.new(); h=w.hero
h.f,h.x,h.y=12,10,11; h.hp,h.atk,h.dfn,h.gold=3745,131,69,1007
# 左袋已清 + 已开 (11,8)(8,6) + 已杀沿途怪
for c in [(12,1,8),(12,2,8),(12,2,7),(12,1,7),(12,3,9),(12,4,11),(12,8,11),(12,3,10),
          (12,11,9),(12,11,7),(12,7,6),(12,11,8),(12,8,6)]:
    w.cleared.add(c)
def can(nx,ny,ky,kb):
    if not(1<=nx<=11 and 1<=ny<=11): return False
    t=w.terrain_at(12,nx,ny)
    if t in (1,2): return w.at(12,nx,ny)==89
    if (nx,ny) in R._stair_cells(w,12): return False
    o=w.at(12,nx,ny)
    if not o: return True
    ty=M.TYPE.get(M.oatr(o,3))
    if o==89 or o==115: return True
    if o in M.KEY_OF or ty in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True
    if ty=='DOOR':
        c=M.DOOR_OF.get(o); return (c=='y' and ky>0) or (c=='b' and kb>0)
    if ty in ('SELL','SAIDAN','MONSTER'):
        if ty=='MONSTER': r=w.battle(o); return r is not None and r[0]<h.hp
        return True
    return False
# 从 (5,5)（8,6 开门后所在区）0钥洪泛
start=(5,5); seen={start}; q=deque([start])
while q:
    cx,cy=q.popleft()
    for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
        nx,ny=cx+dx,cy+dy
        if (nx,ny) in seen: continue
        if can(nx,ny,0,0): seen.add((nx,ny)); q.append((nx,ny))
for k in [(5,1),(7,1),(7,2),(8,1),(1,5),(9,7),(4,5),(1,4)]:
    print('(%d,%d): %s'%(k[0],k[1],'可达' if k in seen else '否'))

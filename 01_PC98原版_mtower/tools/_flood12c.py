import mota_core as M, run_segs as R
from collections import deque
w = M.World.new()
h = w.hero
h.f, h.x, h.y = 12, 10, 11
h.hp, h.atk, h.dfn, h.gold = 3745, 131, 69, 1007
h.keys = {'y':1,'b':0,'r':1}
DIRS = ((0,1),(0,-1),(1,0),(-1,0))
# ① 从落点走到 (3,11) 并模拟开 (3,10) 黄门（消耗黄钥，格清空）
w.set_at(12,3,10,0); w.cleared.add((12,3,10)); h.keys['y']-=1
# ② 从 (3,9)（门内侧）洪泛，0 剩余钥匙
seen = {(3,9)}
q=deque([(3,9)])
while q:
    cx,cy=q.popleft()
    for dx,dy in DIRS:
        nx,ny=cx+dx,cy+dy
        if (nx,ny) in seen: continue
        ok,_=R._cost(w,12,nx,ny)
        if ok: seen.add((nx,ny)); q.append((nx,ny))
def has(x,y): return (x,y) in seen
print('商人(1,1):',has(1,1),'| 暗墙(2,1):',has(2,1),'| 蓝钥(2,8):',has(2,8))
print('黄钥(1,7)(2,7)(1,8):',has(1,7),has(2,7),has(1,8))
print('黄门(1,4):',has(1,4),'| 黄门(4,5):',has(4,5),'| 蓝门(9,8):',has(9,8))
for y in range(1,12):
    s=''
    for x in range(1,12):
        if (x,y) in seen: s+='O'
        else:
            t=w.terrain_at(12,x,y); s+='#' if t in (1,2) else '.'
    print('%2d %s'%(y,s))

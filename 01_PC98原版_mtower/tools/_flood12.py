import mota_core as M, run_segs as R
from collections import deque
w = M.World.new()
h = w.hero
h.f, h.x, h.y = 12, 10, 11
h.hp, h.atk, h.dfn, h.gold = 3745, 131, 69, 1007
h.keys = {'y':0,'b':0,'r':0}   # 0钥匙：只验证无钥可达
print('落地 12F(%d,%d)'%(h.x,h.y), '商店价156 =', M.SHOP_PRICE.get(156))
DIRS = ((0,1),(0,-1),(1,0),(-1,0))
seen = {(h.x,h.y)}
q = deque([(h.x,h.y)])
while q:
    cx,cy = q.popleft()
    for dx,dy in DIRS:
        nx,ny = cx+dx, cy+dy
        if (nx,ny) in seen: continue
        ok,_ = R._cost(w,12,nx,ny)
        if ok:
            seen.add((nx,ny)); q.append((nx,ny))
# 输出：商人、暗墙、关键格是否在无钥可达集
def has(x,y): return (x,y) in seen
print('商人(1,1) 无钥可达:', has(1,1))
print('暗墙(2,1) 无钥可达:', has(2,1))
print('蓝门(9,8) 无钥可达:', has(9,8))
print('蓝钥(2,8) 无钥可达:', has(2,8))
print('黄门(3,10) 无钥可达:', has(3,10))
print('黄门(1,4) 无钥可达:', has(1,4))
print('左袋黄钥(1,7)/(2,7)/(1,8):', has(1,7),has(2,7),has(1,8))
# 打印可达网格
print('--- 无钥可达图 (O=可达, .=不可达, #=墙) ---')
for y in range(1,12):
    s=''
    for x in range(1,12):
        if (x,y) in seen: s+='O'
        else:
            t = w.terrain_at(12,x,y)
            s += '#' if t in (1,2) else '.'
    print('%2d %s'%(y,s))

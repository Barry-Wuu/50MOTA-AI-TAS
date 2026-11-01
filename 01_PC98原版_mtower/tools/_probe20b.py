# -*- coding: utf-8 -*-
"""20F 当前状态（4 区已过 BOSS）：模拟 boss20=True + 20F 段已做的清理，看右下角连通性"""
import sys
from collections import deque
sys.path.insert(0, 'tools')
import mota_core as M

w = M.World.new()
w.apply_floor_events(20)
w.boss20 = True
# 模拟 4 区 20F 段已清：中央 BOSS 区 + (6,9)红门已开 + 外圈晶石已取
# 4 区 20F 段实际清掉的（从 run_segs 889-901）：(6,9)红门→(6,8)→(10,4)蓝药→(6,7)→(6,6)吸血鬼→(6,8)→(6,10)→(6,5)→(6,4)→(6,3)落穴→(6,2)→(6,1)
# + 20b 段：(6,10)→(6,9)→(6,8)→(5,8)→(4,8)→(4,7)→(4,6)→(4,5)→(4,4)→(5,4)→(6,4)→(7,4)→(8,4)→(8,5)→(8,6)→(8,7)→(8,8)→(7,8)→(6,8)
for c in [(20,6,9),(20,6,8),(20,10,4),(20,6,7),(20,6,6),(20,6,5),(20,6,4),(20,6,3),(20,6,2),
          (20,5,8),(20,4,8),(20,4,7),(20,4,6),(20,4,5),(20,4,4),(20,5,4),(20,7,4),(20,8,4),
          (20,8,5),(20,8,6),(20,8,7),(20,8,8),(20,7,8),(20,6,1)]:
    w.cleared.add(c)
w.hero.hp, w.hero.atk, w.hero.dfn = 1189, 170, 137

start = (6, 10)
def can_enter(x, y):
    if not (1<=x<=11 and 1<=y<=11): return False
    if w.terrain_at(20,x,y) in (1,2): return False
    o = w.at(20,x,y)
    if not o: return True
    t = M.TYPE.get(M.oatr(o,3),'?')
    if o in M.KEY_OF or t in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True
    if o in M.DECOR_PASS: return True
    if t=='DOOR':
        col=M.DOOR_OF.get(o); return col is not None and w.hero.keys[col]>0
    if t=='MONSTER':
        r=w.battle(o); return r is not None and r[0]<w.hero.hp
    return False

seen={start}; dq=deque([start])
while dq:
    x,y=dq.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n in seen: continue
        if can_enter(*n): seen.add(n); dq.append(n)

print('=== 20F（4区后）从(6,10)可达 ===')
for y in range(1,12):
    row=[]
    for x in range(1,12):
        o=w.at(20,x,y); t=M.TYPE.get(M.oatr(o,3),'?')
        ch='·'
        if (x,y)==start: ch='@'
        elif (x,y) in seen:
            if o and t=='MONSTER': ch='m'
            elif o and t=='DOOR': ch='d'
            elif o in M.KEY_OF: ch='k'
            elif o: ch='?'
            else: ch='.'
        elif o and t=='MONSTER': ch='M'
        elif o and t=='DOOR': ch='D'
        elif o in M.KEY_OF: ch='k'
        elif o: ch='?'
        elif w.terrain_at(20,x,y)==1: ch='#'
        row.append(ch)
    print('%2d'%y, ' '.join(row))
print('\n可达内怪/门/钥匙/物品:')
for (x,y) in sorted(seen):
    o=w.at(20,x,y)
    if o:
        t=M.TYPE.get(M.oatr(o,3),'?')
        print('  (%d,%d) obj%d %s %s'%(x,y,o,M.oname(o)[:10],t))

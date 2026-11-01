# -*- coding: utf-8 -*-
"""42F 从 (6,10) 出发，允许战斗+开门（钥匙足够），BFS 可达区 + 沿途怪/门/钥匙"""
import sys
from collections import deque
sys.path.insert(0, 'tools')
import mota_core as M

w = M.World.new()
w.apply_floor_events(42)   # 剧情清场已建模（金骑士+4魔導師）

# 模拟 hero 状态
w.hero.hp, w.hero.atk, w.hero.dfn, w.hero.gold = 1189, 170, 137, 780
w.hero.keys['y'], w.hero.keys['b'], w.hero.keys['r'] = 2, 0, 1
start = (6, 10)

def can_enter(x, y):
    """能否踏入（战斗能赢/门有钥/物品可拾）——只判断，不消耗"""
    if not (1 <= x <= 11 and 1 <= y <= 11): return False
    if w.terrain_at(42, x, y) in (1, 2): return False
    o = w.at(42, x, y)
    if not o: return True
    t = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF or t in ('STATUS','ITEM','NORMAL','SCORE','MESSAGE'): return True
    if o in M.DECOR_PASS: return True
    if t == 'DOOR':
        col = M.DOOR_OF.get(o)
        return col is not None and w.hero.keys[col] > 0
    if t == 'MONSTER':
        r = w.battle(o)
        return r is not None and r[0] < w.hero.hp
    return False

seen = {start}; dq = deque([start])
while dq:
    x, y = dq.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(x+dx,y+dy)
        if n in seen: continue
        if can_enter(*n): seen.add(n); dq.append(n)

print('=== 42F 可达（战斗能赢/有钥）==='.ljust(50))
for y in range(1,12):
    row=[]
    for x in range(1,12):
        o=w.at(42,x,y); t=M.TYPE.get(M.oatr(o,3),'?')
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
        elif w.terrain_at(42,x,y)==1: ch='#'
        row.append(ch)
    print('%2d'%y, ' '.join(row))
print('\n可达内需战斗/开门/拾取的格:')
for (x,y) in sorted(seen):
    o=w.at(42,x,y)
    if o:
        t=M.TYPE.get(M.oatr(o,3),'?')
        print('  (%d,%d) obj%d %s  %s'%(x,y,o,M.oname(o)[:10],t))

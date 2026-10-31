# -*- coding: utf-8 -*-
"""从当前 8F(6,2) 状态做可达性 BFS：允许可胜战斗/开门/拾取。记录可达的宝石/血瓶/钥匙/怪。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
# 执行 PREAMBLE + PLAN 到当前 8F(6,2)
_orig = manual.W.move
for d in manual.PREAMBLE_MOVES: _orig(*d)
import route_build as RB
# manual.execute 需要重放 PLAN —— 用 manual 模块的 PLAN
from collections import deque

# 重新构造世界到 8F(6,2)：PREAMBLE + PLAN 全部动作
w = M.World.new()
acts = list(manual.PREAMBLE_MOVES)
# 通过 execute 获取 PLAN 动作
moves2 = list(manual.PREAMBLE_MOVES)
_orig2 = w.move
def rec2(dx, dy):
    lg = _orig2(dx, dy); moves2.append((dx, dy)); return lg
# 手动跑 PLAN（不重放前奏，W 已是前奏态）
w2 = M.World.new()
for d in manual.PREAMBLE_MOVES: w2.move(*d)
w = w2
# 执行 PLAN 动作
plan_moves = []
_o = w.move
def rec3(dx, dy):
    lg = _o(dx, dy); plan_moves.append((dx, dy)); return lg
w.move = rec3
manual.W = w  # 让 manual 用 w
import types
# 重新绑定 manual 的函数引用
manual.execute(verbose=False)
w.move = _o
h = w.hero
print('起点 %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

# BFS：允许打怪（battle 可胜且 HP>0）、开门（有钥匙）、拾取、地板
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
frontier = deque([w])
seen_pos = {(w.hero.f, w.hero.x, w.hero.y)}
pickups = set()
kills = set()
doors = set()
steps = 0
while frontier:
    cur = frontier.popleft()
    for dx, dy in DIRS:
        n = cur.clone()
        lg = n.move(dx, dy)
        if M.blocked(lg): continue
        k = (n.hero.f, n.hero.x, n.hero.y)
        if k in seen_pos: continue
        seen_pos.add(k)
        frontier.append(n)
        # 记录事件
        for e in lg:
            if 'クリスタル' in e or '回復薬' in e or '鍵' in e or '剣' in e or '盾' in e:
                pickups.add((k, e[:40]))
            if '戦' in e and 'た。' in e:
                kills.add(k)
        if len(seen_pos) > 20000: break
    if len(seen_pos) > 20000: break
print('可达位置 %d' % len(seen_pos))
print('含红钥匙(10,2)?', (8,10,2) in seen_pos)
print('含蓝晶(5,11)?', (8,5,11) in seen_pos)
print('含红晶(4,10)?', (8,4,10) in seen_pos)
print('可达拾取:')
for k, e in sorted(pickups):
    print('  ', k, e)

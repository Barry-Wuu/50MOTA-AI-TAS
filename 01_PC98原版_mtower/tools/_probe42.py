# -*- coding: utf-8 -*-
"""诊断：42F 区域结构 + 怪物构成 + 从 (6,10) 的可达性（不消耗，只标可达格）"""
import sys
sys.path.insert(0, 'tools')
import mota_core as M

w = M.World.new()
w.apply_floor_events(42)

# 标注每格：对象类型
def label(o):
    if not o: return '·'
    t = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF: return 'K'
    if t == 'DOOR': return 'D'
    if t == 'MONSTER': return 'M%d' % o
    if t == 'SHOP' or t == 'SELL': return 'S'
    if t == 'STATUS' or t == 'ITEM': return 'I'
    return '?%d' % o

print('=== 42F 布局（事件后）===')
for y in range(1, 12):
    print('%2d' % y, ' '.join('%3s' % label(w.at(42, x, y)) for x in range(1, 12)))

# 怪物清单（事件后）
print('\n=== 42F 怪物（obj: 属性 hp/atk/def/gold）===')
for y in range(1, 12):
    for x in range(1, 12):
        o = w.at(42, x, y)
        if o and M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
            print('  (%d,%d) obj%d %s  hp%d atk%d def%d g%d' % (
                x, y, o, M.oname(o)[:8], M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oatr(o, 13)))

# 钥匙位置
print('\n=== 42F 钥匙 ===')
for y in range(1, 12):
    for x in range(1, 12):
        o = w.at(42, x, y)
        if o in M.KEY_OF:
            print('  (%d,%d) obj%d' % (x, y, o))

# 门位置
print('\n=== 42F 门 ===')
for y in range(1, 12):
    for x in range(1, 12):
        o = w.at(42, x, y)
        if M.TYPE.get(M.oatr(o, 3)) == 'DOOR':
            print('  (%d,%d) obj%d' % (x, y, o))

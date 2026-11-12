# -*- coding: utf-8 -*-
# 探索 V45：从 V44 终点 32F(6,10) 出发，按攻略 line276 第一步 fly(20) 拿血瓶。
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import z2_route, run_segs, mota_core as M

rc = z2_route.main()   # 跑到 V44 终点
w = run_segs.LAST_W
h = w.hero
print('\n=== V44 终点:', z2_route.st(h))

# 20F 血瓶/石头人位置精确 dump（只列关键物件）
print('\n=== 20F 关键物件 ===')
for y in range(1, 12):
    for x in range(1, 12):
        o = w.at(20, x, y)
        if not o:
            continue
        ty = M.TYPE.get(M.oatr(o, 3))
        if ty in ('STATUS', 'ITEM', 'MONSTER', 'KEY') or o in M.DOOR_OF:
            c10, c11, c12 = M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12)
            print('  (%2d,%2d) obj%-3d %-8s %s  HP%s ATK%s DEF%s 价%s' % (
                x, y, o, ty, M.oname(o), c10, c11, c12, M.oatr(o, 13)))

# 32F 楼梯与落点关系
print('\n=== 32F STAIRS:', M.STAIRS[32], ' FLY_LAND[20]=', M.FLY_LAND[20])
print('=== 32F 落点周边: (6,10)=%s (6,9)=%s (6,11)=%s (5,10)=%s (7,10)=%s' % (
    w.at(32, 6, 10), w.at(32, 6, 9), w.at(32, 6, 11), w.at(32, 5, 10), w.at(32, 7, 10)))

# 金騎士 obj90 是否在 (6,9)
o = w.at(32, 6, 9)
print('=== 32F(6,9) obj=%d (%s) —— 判断是否为"先手攻击"金騎士' % (
    o, M.oname(o) if o else '无'))

# 测试 fly(20)：从 32F(6,10) 直接飞（(6,10) 紧邻下梯 (6,11)）
print('\n--- 尝试 fly(20) from 32F(6,10) ---')
lg = w.fly(20)
print(' ', lg)
print(' ', z2_route.st(h))

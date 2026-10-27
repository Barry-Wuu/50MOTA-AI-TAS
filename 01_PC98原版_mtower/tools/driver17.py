#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""driver17.py —— 用提交的 1F→11F 路线作地基，套用 probe15 的 GOALS 延伸序列（已建立的 11F→17F 策略），
验证（a）延伸序列走不走得通；（b）从延伸终态 17F 银剑(17,2,2)/15F 盗贼(15,9,1)/11F 银盾(11,2,2)/13F 神剑(13,6,5) 可达性。
"""
import sys
import state as S
import plan as P
import mota_core as M
import probe15 as PR

w = S.replay('/tmp/committed_route.csv')
print('地基终态(11F):', P.st(w.hero), flush=True)

# 用 probe15 的 GOALS（已建立的延伸策略），需先 parse_goal
goals = [S.parse_goal(g) for g in PR.GOALS]
w2, err = S.apply_seq(w, goals)
if err:
    print('✗ 延伸序列中断:', err)
    print('停在', P.st(w2.hero))
    sys.exit(1)
print('✓ 延伸序列走完，终态:', P.st(w2.hero), flush=True)

# 可达性 BFS（用修正后的 _key）
best, n = S.bfs(w2, cap=600000)
print('BFS 展开 %d；可达 %d 格；楼层 %s' % (n, len(best), sorted(set(p[0] for p in best))), flush=True)
for f, x, y, lab in [(11, 2, 2, '11F 银盾'), (15, 9, 1, '15F 盗贼'), (15, 6, 1, '15F 上梯'),
                     (16, 6, 2, '16F 落点'), (17, 2, 2, '17F 银剑'), (13, 6, 5, '13F 神剑')]:
    if (f, x, y) in best:
        print('  ✅ %-10s %2dF(%d,%d) 到达时 HP%d (%d 步)' % (lab, f, x, y, best[(f, x, y)][0], best[(f, x, y)][1]))
    else:
        print('  ❌ %-10s %2dF(%d,%d) 不可达' % (lab, f, x, y))

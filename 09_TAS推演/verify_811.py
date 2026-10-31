# -*- coding: utf-8 -*-
"""校验 8F→11F 段 CSV 是否 0 误差（复用 replay_csv.replay）。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演')
import replay_csv

fn = r'../09_TAS推演/魔塔1_route_8F到11F_合法.csv'
rows, bad, per, w = replay_csv.replay(fn)
print('文件 %s  记录 %d 行' % (fn, len(rows)))
print('不一致 %d 处' % len(bad))
for b in bad[:30]:
    print('   ', b)
print('--- 首次进入各层时的状态（重放实测）---')
for f in sorted(per):
    d = per[f]
    print('  %2dF step%-5d HP%-5d ATK%-3d DEF%-3d G%-5d 钥%d/%d/%d'
          % (f, d['step'], d['hp'], d['atk'], d['dfn'], d['gold'], d['ky'], d['kb'], d['kr']))
h = w.hero
print('终态 %dF(%d,%d) HP%d ATK%d DEF%d G%d 钥%d/%d/%d'
      % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
         h.keys.get('y', 0), h.keys.get('b', 0), h.keys.get('r', 0)))
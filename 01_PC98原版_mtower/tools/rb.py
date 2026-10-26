#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rb.py —— 受限 BFS：只在指定楼层集合内移动，输出每格最大 HP。
用法: python3 rb.py "12" 12 11        # 先走 seq 再到目标层集合
      python3 rb.py 12                # 直接从 CSV 终态在 {12} 内 BFS
"""
import sys, collections
import state as S
import plan as P
import mota_core as M

def rb(w, floors, cap=600000):
    best = {}
    q = collections.deque([(w, 0)])
    seen = {P._key(w)}
    n = 0
    while q and n < cap:
        cur, d = q.popleft(); n += 1
        for dx, dy, _ in S.DIRS:
            t = cur.clone()
            lg = t.move(dx, dy)
            if M.blocked(lg) or t.hero.hp <= 0: continue
            if t.hero.f not in floors: continue
            k = P._key(t)
            if k in seen: continue
            seen.add(k)
            pos = (t.hero.f, t.hero.x, t.hero.y)
            if pos not in best or best[pos][0] < t.hero.hp: best[pos] = (t.hero.hp, d+1)
            q.append((t, d+1))
    return best, n

def main():
    a = sys.argv[1:]
    seq = []
    floors = set()
    for t in a:
        if t.startswith('F'):
            floors = set(int(x) for x in t[1:].split(','))
        else:
            seq.append(S.parse_goal(t))
    w = S.replay()
    if seq:
        w, err = S.apply_seq(w, seq)
        if err: print('✗', err); return
    print('起点', P.st(w.hero))
    if not floors: floors = {w.hero.f}
    best, n = rb(w, floors)
    print('展开 %d 状态；楼层 %s 内可达 %d 格' % (n, sorted(floors), len(best)))
    for f in sorted(floors):
        rows = [p for p in best if p[0]==f]
        if not rows: continue
        print('--- %dF' % f)
        for y in range(13):
            cells = ['%X:%-4d'%(x, best[(f,x,y)][0]) for x in range(13) if (f,x,y) in best]
            if cells: print('  y=%-2d %s' % (y, ' '.join(cells)))
        print('  本层未可达物件:')
        for y in range(1,12):
            for x in range(1,12):
                o = M.obj_raw(f,x,y)
                if o and (f,x,y) not in best:
                    print('    (%d,%d) obj%d %s' % (x,y,o,M.oname(o)[:20]))

main()

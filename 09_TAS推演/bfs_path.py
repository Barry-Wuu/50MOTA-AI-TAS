# -*- coding: utf-8 -*-
"""精确 BFS 路径：给定 (f,start,goal)，在 free 格（地板/钥匙/补给/NPC/已开门）上找路径。
   输出路径坐标与途经物。用于确认连通性，不自动打怪/开门。"""
import sys
from collections import deque
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

w = M.World.new()
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def is_free(f, x, y):
    if not (0 <= x < 13 and 0 <= y < 13): return False
    t = w.terrain_at(f, x, y)
    if t == 1 or t == 2: return False
    o = w.at(f, x, y)
    if o == 0: return True
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if o in M.KEY_OF: return True
    if ty in ('STATUS', 'ITEM', 'NORMAL', 'SCORE', 'MESSAGE'): return True
    return False

def path(f, start, goal):
    if start == goal: return []
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        for d in DIRS:
            n = (c[0]+d[0], c[1]+d[1])
            if n in prev: continue
            if not is_free(f, n[0], n[1]): continue
            prev[n] = (c, d)
            if n == goal:
                p = []
                while prev[n] is not None:
                    p.append(n); n = prev[n][0]
                return list(reversed(p))
            q.append(n)
    return None

if __name__ == '__main__':
    f = int(sys.argv[1]); sx, sy = int(sys.argv[2]), int(sys.argv[3])
    gx, gy = int(sys.argv[4]), int(sys.argv[5])
    p = path(f, (sx, sy), (gx, gy))
    if p is None:
        print('无路径 %dF(%d,%d) -> %dF(%d,%d)' % (f, sx, sy, f, gx, gy))
    else:
        print('路径 %d 步:' % len(p))
        cur = (sx, sy)
        out = [cur]
        for n in p:
            d = (n[0]-cur[0], n[1]-cur[1])
            out.append(n); cur = n
        print(' -> '.join('(%d,%d)' % c for c in out))
        # 途经物
        for (x, y) in p:
            o = w.at(f, x, y)
            if o:
                ty = M.TYPE.get(M.oatr(o,3),'?')
                if ty in ('STATUS','ITEM') or o in M.KEY_OF:
                    print('   途经 (%d,%d): %s' % (x, y, M.oname(o)[:25]))

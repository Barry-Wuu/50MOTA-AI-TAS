# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

start = M.World.new()
frontier = collections.deque([start])
seen = {(start.hero.f,start.hero.x,start.hero.y)}
while frontier:
    w = frontier.popleft()
    for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
        w2 = w.clone()
        log = w2.move(dx,dy)
        blk = M.blocked(log)
        k = (w2.hero.f,w2.hero.x,w2.hero.y)
        if blk:
            print('  blocked from (%d,%d) move%s -> %s' % (w.hero.x,w.hero.y,(dx,dy), log[:1]))
            continue
        if k in seen: continue
        seen.add(k); frontier.append(w2)
        print('  OK -> %dF(%d,%d) hp=%d' % (w2.hero.f,w2.hero.x,w2.hero.y,w2.hero.hp))
print('seen:', sorted(seen))

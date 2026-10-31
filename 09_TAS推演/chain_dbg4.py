# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

# 从起始世界做 BFS，允许所有非 blocked 的 move（真实验证能到几层）
start = M.World.new()
frontier = collections.deque([start])
seen_pos = {start._key if False else (start.hero.f,start.hero.x,start.hero.y): start}
# 用 (f,x,y) 做去重键；世界状态含钥匙/HP，这里仅看位置可达性
seen = {(start.hero.f,start.hero.x,start.hero.y)}
maxf = start.hero.f
steps = 0
while frontier:
    w = frontier.popleft()
    maxf = max(maxf, w.hero.f)
    for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
        w2 = w.clone()
        log = w2.move(dx,dy)
        if M.blocked(log): continue
        k = (w2.hero.f,w2.hero.x,w2.hero.y)
        if k in seen: continue
        seen.add(k)
        frontier.append(w2)
        steps+=1
        if len(seen) % 2000 == 0:
            print('  ... reachable %d states, frontier %d, maxf=%d' % (len(seen), len(frontier), maxf))
    if len(seen) > 60000: print('  cap reachable'); break
print('可达位置数', len(seen), 'maxf=', maxf, 'edges=', steps)
# 各层可达数
from collections import Counter
print('每层可达:', dict(sorted(Counter(k[0] for k in seen).items())))

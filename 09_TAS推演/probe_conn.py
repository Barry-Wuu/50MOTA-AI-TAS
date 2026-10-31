# -*- coding: utf-8 -*-
import sys, collections
sys.path.insert(0, r"D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools")
import mota_core as M

# 纯连通性：2F 栅栏门 obj19 视为墙，其余非墙格可走（忽略怪/门/钥匙）
start=(4,8)
seen={start}; q=collections.deque([start])
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=x+dx,y+dy
        if not(0<=nx<13 and 0<=ny<13): continue
        if M.terrain(2,nx,ny)==1: continue
        o=M.obj_raw(2,nx,ny)
        if o==19: continue          # 栅栏门当墙
        if (nx,ny) not in seen:
            seen.add((nx,ny)); q.append((nx,ny))
print("从牢房(4,8)可达格数:", len(seen))
print("奖励NPC(11,4)可达?", (11,4) in seen, " (11,7)可达?", (11,7) in seen)
print("門番B(6,2)可达?", (6,2) in seen, " (8,2)可达?", (8,2) in seen)
print("门后蓝药(3,10)可达?", (3,10) in seen)
# 打印可达区域
for y in range(13):
    line=''
    for x in range(13):
        if (x,y) in seen: line+=' . '
        else:
            t=M.terrain(2,x,y)
            line+= ' # ' if t==1 else ' o '
    print('y%2d '%y+line)

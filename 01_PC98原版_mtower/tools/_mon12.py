import mota_core as M, run_segs as R
w = M.World.new()
h = w.hero
h.f,h.x,h.y=12,10,11
h.hp,h.atk,h.dfn,h.gold=3745,131,69,1007
print('12F 怪物（x,y): id 类型 [hp/atk/def] 可杀')
for y in range(1,12):
    for x in range(1,12):
        o=w.at(12,x,y)
        if not o: continue
        ty=M.TYPE.get(M.oatr(o,3))
        if ty=='MONSTER':
            a=M.oatr(o,10); b=M.oatr(o,11); c=M.oatr(o,12)
            r=w.battle(o)
            ok = r is not None and r[0]<h.hp
            print('  (%d,%d) id%d %s  hp%d atk%d def%d  -> 损%d 可杀:%s'%(x,y,o,M.oname(o)[:12],a,b,c,(r[0] if r else -1),ok))

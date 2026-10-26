import sys
sys.path.insert(0,'/tmp/motarepo2/01_PC98原版_mtower/tools')
import state as S, mota_core as M
w = S.replay()
for f in (11,12,14,15,16,17):
    dead=[]; alive=[]
    for y in range(1,12):
        for x in range(1,12):
            o = M.obj_raw(f,x,y)
            if not o: continue
            if M.TYPE.get(M.oatr(o,3))!='MONSTER': continue
            (dead if (f,x,y) in w.cleared else alive).append('(%d,%d)%s'%(x,y,M.oname(o)[:8]))
    print('%2dF 已死: %s' % (f, ' '.join(dead) or '无'))
    print('    存活: %s' % (' '.join(alive) or '无'))

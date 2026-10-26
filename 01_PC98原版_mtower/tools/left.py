import sys
sys.path.insert(0,'/tmp/motarepo2/01_PC98原版_mtower/tools')
import state as S, mota_core as M
w = S.replay()
print('终态', S.P.st(w.hero))
print('已清 STATUS/ITEM/KEY 格：')
for f in range(1,18):
    got=[]
    for y in range(1,12):
        for x in range(1,12):
            o = M.obj_raw(f,x,y)
            if not o: continue
            t = M.oatr(o,3)
            if M.TYPE.get(t) not in ('STATUS','ITEM','KEY'): continue
            if (f,x,y) in w.cleared: got.append('(%d,%d)obj%d'%(x,y,o))
    if got: print(' %2dF 已捡: %s' % (f, ' '.join(got)))
print()
print('未捡 STATUS/ITEM/KEY（即可用资源）：')
for f in range(1,18):
    left=[]
    for y in range(1,12):
        for x in range(1,12):
            o = M.obj_raw(f,x,y)
            if not o: continue
            t = M.oatr(o,3)
            if M.TYPE.get(t) not in ('STATUS','ITEM','KEY'): continue
            if (f,x,y) not in w.cleared: left.append('(%d,%d)obj%d[%s]'%(x,y,o,M.oname(o)[:12]))
    if left: print(' %2dF: %s' % (f, ' '.join(left)))

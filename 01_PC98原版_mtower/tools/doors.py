import sys
sys.path.insert(0,'/tmp/motarepo2/01_PC98原版_mtower/tools')
import mota_core as M
print('DOOR_OF', M.DOOR_OF)
for f in range(1,20):
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f,x,y)
            if o in (27,):   # 红门
                print('%2dF(%d,%d) obj%d %s' % (f,x,y,o,M.oname(o)[:30]))
            if M.TYPE.get(M.oatr(o,3))=='DOOR':
                pass
# 全部门颜色分布
import collections
c = collections.Counter()
for f in range(1,50):
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f,x,y)
            if M.TYPE.get(M.oatr(o,3))=='DOOR':
                c[M.DOOR_OF.get(o,'?obj%d'%o)] += 1
print('门颜色分布(1-49F):', dict(c))

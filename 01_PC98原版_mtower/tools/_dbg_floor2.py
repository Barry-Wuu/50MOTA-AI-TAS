import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mota_core as M
for f in (40, 41, 33, 34, 35):
    print('='*60); print('FLOOR %d  STAIRS=%s FLY_LAND=%s' % (f, M.STAIRS.get(f), M.FLY_LAND.get(f)))
    for y in range(1, 12):
        line = '%2d  ' % y
        for x in range(1, 12):
            t = M.terrain(f, x, y); o = M.obj_raw(f, x, y)
            if t == 2: line += 'S  '
            elif t == 1: line += '#  '
            elif o == 0: line += '.  '
            else: line += '%-3d' % o
        print(line)
    print('  objects:')
    for y in range(1,12):
        for x in range(1,12):
            o = M.obj_raw(f,x,y)
            if o==0 or M.terrain(f,x,y)==2: continue
            ty = M.TYPE.get(M.oatr(o,3)); ex=''
            if ty=='MONSTER': ex=' hp/atk/def=%s'%(tuple(M.oatr(o,k) for k in (10,11,12)),)
            elif ty=='DOOR': ex=' col=%s'%M.DOOR_OF.get(o)
            elif ty=='KEY': ex=' col=%s'%M.KEY_OF.get(o)
            elif ty in ('SELL','BUY'): ex=' price=%s grant=%s'%(M.SHOP_PRICE.get(o), M.SHOP_GRANT.get(o))
            print('    (%2d,%2d) obj%-3d %-8s %s%s'%(x,y,o,ty,M.oname(o),ex))
    print()

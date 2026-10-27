# -*- coding: utf-8 -*-
import routelib as R, mota_core as M, sys, collections
for f in [int(a) for a in sys.argv[1:]]:
    fl=R.Floor(f)
    print('='*90); print('FLOOR %d'%f)
    for i in range(len(fl.regcells)):
        outs=collections.defaultdict(list)
        for (c,o) in fl.adj[i]:
            b=fl.blocker[c]
            if b[0]=='m':
                info='怪%s(hp%d/atk%d/def%d)'%(M.oname(b[1]),M.oatr(b[1],10),M.oatr(b[1],11),M.oatr(b[1],12))
            else:
                info='门%s'%b[1]
            outs[o].append('%s@%d,%d'%(info,c[0],c[1]))
        if outs:
            print(' 区%-2d → %s'%(i,' ; '.join('区%d[%s]'%(o,', '.join(v)) for o,v in sorted(outs.items()))))

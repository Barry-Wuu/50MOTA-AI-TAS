# -*- coding: utf-8 -*-
import routelib as R, mota_core as M, collections, sys
for f in [int(a) for a in sys.argv[1:]]:
    fl=R.Floor(f)
    print('='*80); print('FLOOR %d  区数=%d'%(f,len(fl.regcells)))
    for i,cells in enumerate(fl.regcells):
        g=fl.gain[i]
        tags=[]
        for (x,y) in sorted(cells):
            o=fl.w.at(f,x,y)
            if not o: continue
            ty=M.TYPE.get(M.oatr(o,3),'?')
            if ty=='STATUS':
                hp,atk,dfn=M.oatr(o,10),M.oatr(o,11),M.oatr(o,12)
                tags.append('(%d,%d)%s'%(x,y,('血+%d'%hp) if hp else ('攻+%d'%atk) if atk else ('防+%d'%dfn) if dfn else M.oname(o)[:4]))
            elif ty=='KEY': tags.append('(%d,%d)钥%s'%(x,y,M.KEY_OF[o]))
        bnd=collections.Counter()
        for (c,o) in fl.adj[i]:
            b=fl.blocker[c]
            if b[0]=='m': bnd['怪%s(hp%d,def%d)'%(M.oname(b[1])[:4],M.oatr(b[1],10),M.oatr(b[1],12))]+=1
            else: bnd['门'+b[1]]+=1
        st=[(x,y) for (x,y) in sorted(cells) if (x,y) in fl.stair]
        print(' 区%-2d n=%-3d %s'%(i,len(cells),' '.join('%d,%d'%(x,y) for x,y in sorted(cells))))
        if tags: print('      物: '+' '.join(tags))
        if st: print('      梯: %s'%st)
        print('      界: '+' | '.join('%s×%d'%(k,v) for k,v in sorted(bnd.items())))

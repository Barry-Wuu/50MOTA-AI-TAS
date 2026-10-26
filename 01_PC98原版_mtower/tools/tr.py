import sys, csv
sys.path.insert(0,'/tmp/motarepo2/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()
rows = list(csv.reader(open('route_plan.csv', encoding='utf-8')))[1:]
DM = {'8':(0,-1),'6':(1,0),'2':(0,1),'4':(-1,0)}
prev_f = 1
loss_f = 0
print('step  f   (x,y)    HP    ΔHP   ATK DEF  事件')
for r in rows:
    if len(r) < 7: continue
    try:
        st = int(r[0])
    except: continue
    k = r[4]
    dx,dy = DM.get(k,(0,0))
    if dx==0 and dy==0: continue
    h0 = w.hero.hp
    lg = w.move(dx,dy)
    d = w.hero.hp - h0
    if d < -20 or w.hero.f != prev_f:
        print('%4d %2dF (%d,%d) %5d %+5d  %d/%d  %s' % (st, w.hero.f, w.hero.x, w.hero.y, w.hero.hp, d, w.hero.atk, w.hero.dfn, ' | '.join(lg)[:60]))
    prev_f = w.hero.f
print('终态', w.hero.f, (w.hero.x,w.hero.y), 'HP',w.hero.hp,'ATK',w.hero.atk,'DEF',w.hero.dfn,'G',w.hero.gold)

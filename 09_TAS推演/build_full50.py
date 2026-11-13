# -*- coding: utf-8 -*-
"""跑 z2_route.main() 全 50F，录制逐格状态 → merged_route_full.json

录制三层：
  · steps：每次 move/fly/wing_up/wing_down 的前后状态、方向、日志
  · cons ：被消耗的格（击杀/拾取/开门/撞暗墙）→ 渲染时还原成地面
  · dyn  ：**新出现/变化的格**（set_at / ter_over）→ 渲染时从该步起显示（10F 楼梯、41F 暗墙与道具等）
"""
import io, os, sys, json, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
os.chdir(TOOLS)
import mota_core as M
import z2_route as Z
import run_segs

DIRV = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', (0, 0): '·'}


def snap(h):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0),
                items=sorted(h.items))


steps = []
cons = collections.defaultdict(list)      # f -> [[x,y,step,tile]]
dyn = collections.defaultdict(list)       # f -> [[x,y,step,obj]]
prev = snap(M.Hero.initial())
cleared_prev = set()
over_prev = {}
ter_prev = {}


def _tile(f, x, y):
    s = M.STAIRS.get(f) or ()
    return 'ku' if (x, y) == (s[0] if len(s) > 0 else None) else 'f'


def record(w, d, lg):
    global prev, cleared_prev, over_prev, ter_prev
    h = w.hero
    a = snap(h)
    idx = len(steps) + 1
    log = ' ｜ '.join(x for x in (lg or []) if x)
    steps.append(dict(i=idx, s='A', f=h.f, x=h.x, y=h.y,
                      d='·' if d is None else DIRV.get(tuple(d), '·'),
                      e='', l=log,
                      hp=a['hp'], a=a['atk'], df=a['dfn'], g=a['gold'],
                      ky=a['ky'], kb=a['kb'], kr=a['kr'],
                      dh=a['hp'] - prev['hp'], da=a['atk'] - prev['atk'],
                      dd=a['dfn'] - prev['dfn'], dg=a['gold'] - prev['gold'], st='ok'))
    for (cf, cx, cy) in sorted(w.cleared - cleared_prev):
        cons[str(cf)].append([cx, cy, idx, _tile(cf, cx, cy)])
    cleared_prev = set(w.cleared)
    for k, v in w.over.items():
        if over_prev.get(k) != v and v and k not in w.cleared:
            dyn[str(k[0])].append([k[1], k[2], idx, int(v) if isinstance(v, int) else str(v)])
    for k, v in w.ter_over.items():
        if ter_prev.get(k) != v:
            dyn[str(k[0])].append([k[1], k[2], idx, 'T%d' % v])
    over_prev = dict(w.over)
    ter_prev = dict(w.ter_over)
    prev = a


_om = M.World.move
def move_rec(self, dx, dy):
    lg = _om(self, dx, dy)
    record(self, (dx, dy), lg)
    return lg
M.World.move = move_rec

_of = M.World.fly
def fly_rec(self, tf):
    lg = _of(self, tf)
    record(self, None, lg)
    return lg
M.World.fly = fly_rec

for _nm in ('wing_up', 'wing_down'):
    _o = getattr(M.World, _nm)
    def _mk(o):
        def f(self, *a, **k):
            lg = o(self, *a, **k)
            record(self, None, lg)
            return lg
        return f
    setattr(M.World, _nm, _mk(_o))

# ✅ 2026-11-13 修正：先录真实起点步（Hero.initial() 的 1F(6,11)，初始状态）。
#   此前 z2_route.main() 的第一个 record 是"第一个移动后"的位置（1F(5,11)），
#   起点 (6,11) 从未被录成 step0 → 前端把 (5,11) 当起点渲染，勇者开场即错位一格。
h0 = M.Hero.initial()
a0 = snap(h0)
steps.append(dict(i=1, s='A', f=h0.f, x=h0.x, y=h0.y,
                  d='·', e='', l='',
                  hp=a0['hp'], a=a0['atk'], df=a0['dfn'], g=a0['gold'],
                  ky=a0['ky'], kb=a0['kb'], kr=a0['kr'],
                  dh=0, da=0, dd=0, dg=0, st='ok'))

rc = Z.main()
print('=== main rc=%s  steps=%d ===' % (rc, len(steps)))

fids = sorted(set(s['f'] for s in steps))
TYPECH = {'MONSTER': 'm', 'DOOR': 'd', 'STATUS': 'i', 'ITEM': 'i',
          'MESSAGE': 'n', 'SCORE': 's', 'SAIDAN': 'a', 'SELL': 's'}
floors = {}
base = M.base_cells()

# terrain 用最终 World 的动态口径（terrain_at），反映运行时真实开墙：
#   DIG_WALLS 凿墙、DARKWALL 撞塌暗墙、obj89 撞塌、37F 镐破墙、24F 秘道、38F 撞墙等。
#   ⚠️ 2026-11-13 v11：删除了"走过的格一律标记为地板"的反推逻辑（原 138-149 行）。
#   该逻辑会把路线本身的错误合法化（如 OPEN_WALLS 穿墙），只应保留引擎真实动态变更。
_w = run_segs.LAST_W
def _dyn_terrain(f, x, y):
    return _w.terrain_at(f, x, y)

for f in fids:
    floors[str(f)] = dict(
        steps=0, loss=0, kills=0, doors=0, pickups=0, visits=0,
        entry=None, exit=None,
        terrain=[[_dyn_terrain(f, x, y) for x in range(13)] for y in range(13)],
        objs={}, path=[], minhp=None, mincell=None,
        monsters={}, doorcol={}, picklist={}, special=[],
        reached=False, exec_steps=0)
for (ff, x, y), o in base.items():
    k = str(ff)
    if k not in floors:
        continue
    t = M.TYPE.get(M.oatr(o, 3))
    floors[k]['objs']['%d,%d' % (x, y)] = [o, M.oname(o)[:24], TYPECH.get(t, 'o')]

# ⚠️ 2026-11-13 v11：删除"走过格一律标地板"的反推逻辑。
#   原逻辑把路线成功经过的格子 terrain 强制设 0，会合法化路线里的穿墙错误
#   （如已撤销的 OPEN_WALLS）。terrain 现在完全由 _dyn_terrain（引擎真值）决定。

for s in steps:
    fd = floors[str(s['f'])]
    fd['steps'] += 1
    fd['reached'] = True
    fd['exec_steps'] += 1
    if fd['entry'] is None:
        fd['entry'] = dict(hp=s['hp'] - s['dh'], atk=s['a'] - s['da'], dfn=s['df'] - s['dd'],
                           gold=s['g'] - s['dg'], ky=s['ky'], kb=s['kb'], kr=s['kr'], items=[])
    fd['exit'] = dict(hp=s['hp'], atk=s['a'], dfn=s['df'], gold=s['g'],
                      ky=s['ky'], kb=s['kb'], kr=s['kr'], items=[])
    if s['dh'] < 0:
        fd['loss'] += -s['dh']
        if fd['minhp'] is None or s['hp'] < fd['minhp']:
            fd['minhp'] = s['hp']
            fd['mincell'] = [s['x'], s['y']]
    if '击杀' in s['l']:
        fd['kills'] += 1
        for part in s['l'].split('击杀')[1:]:
            nm = part.strip().split(' ')[1] if len(part.strip().split(' ')) > 1 else '?'
            fd['monsters'][nm] = fd['monsters'].get(nm, 0) + 1
    if '门 obj' in s['l'] and '开' in s['l']:
        fd['doors'] += 1
        for col, cn in (('黄门', '黄'), ('蓝门', '蓝'), ('红门', '红')):
            if col in s['l']:
                fd['doorcol'][cn] = fd['doorcol'].get(cn, 0) + 1
    if '拾' in s['l']:
        fd['pickups'] += 1
    p = [s['x'], s['y']]
    if not fd['path'] or fd['path'][-1] != p:
        fd['path'].append(p)

# BOSS 死后现出上行梯：引擎走 warp 分支、不改 terrain/over → 手工补 dyn
STAIR_APPEAR = [('10F(6,11) 将生上行梯', 10, 6, 11),
                ('20F(6,1) 现出上行梯', 20, 6, 1),
                ('落穴消失，(6,1) 现上行梯', 30, 6, 1),
                ('40F(6,1) 将现出上行梯', 40, 6, 1)]
for s in steps:
    for (pat, f2, x2, y2) in STAIR_APPEAR:
        if pat in s['l']:
            dyn[str(f2)].append([x2, y2, s['i'], 'STAIR'])
            break

monstats = {}
objnames = {}
for oid in range(len(M.OA)):
    if oid == 0:
        continue
    try:
        objnames[str(oid)] = M.oname(oid)[:10]
    except Exception:
        pass
    if M.oatr(oid, 3) == 6:
        a = M.OA[oid]
        monstats[str(oid)] = [a[10], a[11], a[12], M.oname(oid)[:24]]

total = dict(steps=len(steps),
             loss=sum(max(0, -s['dh']) for s in steps),
             kills=sum(1 for s in steps if '击杀' in s['l']),
             doors=sum(1 for s in steps if '门 obj' in s['l'] and '开' in s['l']),
             pickups=sum(1 for s in steps if '拾' in s['l']))
last = steps[-1]
final = dict(hp=last['hp'], atk=last['a'], dfn=last['df'], gold=last['g'],
             ky=last['ky'], kb=last['kb'], kr=last['kr'], items=[])
mi = min(steps, key=lambda s: (s['hp'], s['i']))
minhp = [mi['hp'], mi['f'], mi['x'], mi['y'], mi['i']]

data = dict(total=total, segs={}, floors=floors, steps=steps, issues=[],
            final=final, minhp=minhp, markers={}, dead=None, blocked=None,
            verify={}, monstats=monstats, objnames=objnames,
            cons={k: v for k, v in cons.items()},
            dyn={k: v for k, v in dyn.items()})

out = DED + 'merged_route_full.json'
json.dump(data, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('written', out)
print('steps', len(steps), 'floors', len(floors),
      'cons floors', len(cons), 'dyn entries', sum(len(v) for v in dyn.values()))
print('final', final, 'minhp', minhp)
print('dyn floors:', sorted(dyn.keys(), key=lambda z: int(z)))

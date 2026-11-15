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


def snap(h, w=None):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0),
                items=sorted(h.items),
                cw=(w.center_warp_charges if w is not None else 0))


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
    a = snap(h, w)
    idx = len(steps) + 1
    log = ' ｜ '.join(x for x in (lg or []) if x)
    steps.append(dict(i=idx, s='A', f=h.f, x=h.x, y=h.y,
                      d='·' if d is None else DIRV.get(tuple(d), '·'),
                      e='', l=log,
                      hp=a['hp'], a=a['atk'], df=a['dfn'], g=a['gold'],
                      ky=a['ky'], kb=a['kb'], kr=a['kr'],
                      it=a['items'], cw=a['cw'],
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
            # ⚠️ ter_over 存的是 **MA 索引**，不是地形类别：ter_over=1 → MA[1][3]=0 → 地板；
            #   ter_over=3 → MA[3][3]=1 → 暗墙；ter_over=31（24F 复原）→ MA[31][3]=1 → 墙。
            #   旧代码直接 'T%d' % v 把索引当地形类别发出，导致 37F 整层凿开的墙（v=1）
            #   被前端标成「T1=墙」，画出来仍是墙 ← 用户 2026-11-15 指出的 bug。
            #   现在统一发出地形类别 0/1/2，仅保留 v==3 的「暗墙」特例（前端有独立紫色标签）。
            tc = M.MA[v][3] if 0 <= v < len(M.MA) else 1
            code = 3 if v == 3 else tc
            dyn[str(k[0])].append([k[1], k[2], idx, 'T%d' % code])
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

# ✅ 2026-11-15：道具使用也单独录一步。此前 use_super_pick()/use_bomb() 等直接调用、
#   不产生 step，导致 37F「超级镐破整层 45 格真墙」这个关键动作被记到下一个移动步头上
#   （日志里完全没有"使用超级镐"），前端也看不到它引发的整层地形变化。
#   现统一包一层：调用后立刻 record 一个 d='·' 的原地步，日志即该方法返回的 lg。
for _nm in ('use_super_pick', 'use_pick', 'use_bomb', 'use_snow_crystal', 'use_elixir'):
    if not hasattr(M.World, _nm):
        continue
    _o = getattr(M.World, _nm)
    def _mk2(o):
        def f(self, *a, **k):
            h = self.hero
            before = (len(self.cleared), len(self.over), len(self.ter_over),
                      h.hp, h.atk, h.dfn)
            r = o(self, *a, **k)
            # 失败（ok=False，如"没有圣水"）不记步，避免终点冒出一条失败日志步
            if isinstance(r, tuple) and r and r[0] is False:
                return r
            after = (len(self.cleared), len(self.over), len(self.ter_over),
                     h.hp, h.atk, h.dfn)
            # 完全没改变任何状态（如雪之结晶"四邻无熔岩"）也不记步
            if before == after:
                return r
            lg = r[1] if isinstance(r, tuple) and len(r) > 1 else None
            record(self, None, lg if isinstance(lg, (list, tuple)) else None)
            return r
        return f
    setattr(M.World, _nm, _mk2(_o))

# ✅ 2026-11-13 修正：先录真实起点步（Hero.initial() 的 1F(6,11)，初始状态）。
#   此前 z2_route.main() 的第一个 record 是"第一个移动后"的位置（1F(5,11)），
#   起点 (6,11) 从未被录成 step0 → 前端把 (5,11) 当起点渲染，勇者开场即错位一格。
h0 = M.Hero.initial()
a0 = snap(h0, None)
steps.append(dict(i=1, s='A', f=h0.f, x=h0.x, y=h0.y,
                  d='·', e='', l='',
                  hp=a0['hp'], a=a0['atk'], df=a0['dfn'], g=a0['gold'],
                  ky=a0['ky'], kb=a0['kb'], kr=a0['kr'],
                  it=a0['items'], cw=a0['cw'],
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

# 道具中文标准译名（萌娘百科/搜狗百科标准译法，覆盖日文原名）
ITEM_CN = {
    25: '记事本',      # 知恵のオーブ Orb of Wisdom
    26: '楼层传送器',  # 飛翔のオーブ Orb of Fly
    39: '神圣盾',      # 神　盾 Sacred Shield
    103: '十字架',     # 十字架 Cross
    104: '圣水',       # エリクサー Elixir
    105: '破坏之玉',   # 破壊の玉 Bomb
    106: '中心对称飞行器',  # 空間転移の秘宝 Central Symmetry Flight Device
    107: '上楼器',     # 昇華の翼 Up-floorer
    108: '下楼器',     # 降臨の翼 Down-floorer
    109: '屠龙匕',     # ドラゴンスレーヤー Dragon Slayer
    110: '冰冻魔法',   # 雪の結晶 Snow Crystal
    111: '魔法钥匙',   # 魔法の鍵 Magic Key
    112: '地震卷轴',   # スーパーマトック Super Magic Mattok (地震卷轴)
    113: '幸运金币',   # 幸運の金貨 Lucky Gold Coin
    114: '镐',         # マトック Magic Mattok
}
for k, v in ITEM_CN.items():
    objnames[str(k)] = v

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

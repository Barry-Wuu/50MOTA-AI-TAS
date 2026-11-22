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

# ✅ 2026-11-15：勇者朝向沿用。非移动步（fly / wing_* / 道具使用 / 商店 / 祭坛）
#   本来传 d=None，旧代码一律记成 '·' —— 前端看就是"勇者不知道朝哪"。
#   原版传送和用道具都不改朝向，所以这些步沿用上一个移动步的朝向。
last_dir = ['↑']


def snap(h, w=None):
    # ✅ 2026-11-20：V83 清扫期间 z2_route 临时清零钥匙做「无钥绕门」寻路，
    #   录制步数时若看到 sweep_real_keys 掩码，则显示真实钥匙——
    #   否则前端会看到钥匙在清扫段「凭空消失又回来」（用户：#4410 黄钥匙不翼而飞）。
    _mask = getattr(w, 'sweep_real_keys', None) if w is not None else None
    if _mask is not None:
        _ky, _kb, _kr = _mask
        _ky += h.keys.get('y', 0); _kb += h.keys.get('b', 0); _kr += h.keys.get('r', 0)
    else:
        _ky = h.keys.get('y', 0); _kb = h.keys.get('b', 0); _kr = h.keys.get('r', 0)
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=_ky, kb=_kb, kr=_kr,
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


def record(w, d, lg, face=None):
    global prev, cleared_prev, over_prev, ter_prev
    h = w.hero
    a = snap(h, w)
    idx = len(steps) + 1
    log = ' ｜ '.join(x for x in (lg or []) if x)
    if face is not None:
        # ✅ 2026-11-22（用户：「买完东西脸不朝向祭坛」）：面朝目标格的原地步，
        #   朝向必须由「英雄格 → 目标格」推导（如 32F 人站 (10,11) 面朝祭坛 (10,10) = ↑），
        #   不能沿用上一步移动方向（否则从左走来就一直朝 →）。face_* 三类原地步都传此参。
        fx, fy = face
        _d = DIRV.get((fx - h.x, fy - h.y)) or last_dir[0]
        if _d != '·':
            last_dir[0] = _d
    elif d is None:                     # 非移动步：沿用上一个朝向
        _d = last_dir[0]
    else:
        _dv = DIRV.get(tuple(d))
        if _dv and _dv != '·':
            last_dir[0] = _dv
            _d = _dv
        else:
            _d = last_dir[0]
    steps.append(dict(i=idx, s='A', f=h.f, x=h.x, y=h.y,
                      d=_d,
                      e='', l=log,
                      hp=a['hp'], a=a['atk'], df=a['dfn'], g=a['gold'],
                      ky=a['ky'], kb=a['kb'], kr=a['kr'],
                      it=a['items'], cw=a['cw'],
                      dh=a['hp'] - prev['hp'], da=a['atk'] - prev['atk'],
                      dd=a['dfn'] - prev['dfn'], dg=a['gold'] - prev['gold'], st='ok'))
    for (cf, cx, cy) in sorted(w.cleared - cleared_prev):
        cons[str(cf)].append([cx, cy, idx, _tile(cf, cx, cy)])
        # ✅ 2026-11-16（用户指出：撞塌暗墙后该格未显示为地面）：
        #   obj89「壁がくずれた」这类隐形墙/暗墙踩上即塌，靠 cons 只贴地板层，
        #   但 dyn 没有「地形变地面」记录 → 悬停无说明、且与「墙→地面」语义脱节。
        #   这里对被撞塌的墙/暗墙格补发 T0（前端 consumeLayer 会贴本层地板贴图）。
        if M.obj_raw(cf, cx, cy) == 89 or (cf, cx, cy) in M.DARKWALL_CELLS:
            if not any(d[2] == idx and d[3] == 'T0' for d in dyn[str(cf)] if d[0] == cx and d[1] == cy):
                dyn[str(cf)].append([cx, cy, idx, 'T0'])
    cleared_prev = set(w.cleared)
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
    # ✅ 2026-11-19：地形事件先发、物件事件后发 —— 同一步里「格子从墙变地板 + 站上去一只怪」
    #   （10F 围杀 (5,6)(7,6)）必须让物件排在后面，前端按「该格最后一条事件」判定才不会把怪压掉。
    for k, v in w.over.items():
        # ✅ 2026-11-16：原条件里的 `and v` 把 over=0（格子被清成地面）整类事件丢掉了，
        #   导致 10F BOSS 后 (4,4)(8,4)(6,7) 三个落穴被拆掉，前端却仍画成落穴（用户指出地面渲染错误）。
        #   现在 over 由「有物件」变成 0 时也发一条 'T0'（地形=地面），前端 consumeLayer 会贴地板贴图。
        if over_prev.get(k) != v and k not in w.cleared:
            if v:
                dyn[str(k[0])].append([k[1], k[2], idx, int(v) if isinstance(v, int) else str(v)])
            elif over_prev.get(k) or M.obj_raw(k[0], k[1], k[2]):
                # ✅ 2026-11-19：静态格（cells 里的怪/物件）被 set_at(...,0) 抹掉时，
                #   over_prev 里没有它的旧值（静态物件不在 over 里），旧条件会漏发 T0
                #   → 前端仍按 objs 把那只怪画在原地。40F 剧本「怪走到 (6,6) 后原格腾空」
                #   正是这种情形，故补 obj_raw 判据。
                dyn[str(k[0])].append([k[1], k[2], idx, 'T0'])
    over_prev = dict(w.over)
    ter_prev = dict(w.ter_over)
    prev = a


_om = M.World.move
def move_rec(self, dx, dy):
    lg = _om(self, dx, dy)
    record(self, (dx, dy), lg)
    # ✅ 2026-11-19：40F 踩 (6,7) 触发围杀剧本时，引擎只登记 pending，
    #   这里在「到达步」之后逐波补记 13 个零位移步（每步一只怪走过来出手），
    #   这样掉血分散在各自那一步、前端能逐步看到怪消失。
    if getattr(self, 'cut40_pending', False):
        self.cut40_pending = False
        for _wlg in self.iter_cut40():
            record(self, None, _wlg)
    return lg
M.World.move = move_rec
M.DEFER_CUT_STEPS = True

_of = M.World.fly
def fly_rec(self, tf):
    lg = _of(self, tf)
    record(self, None, lg)
    return lg
M.World.fly = fly_rec

# ✅ 2026-11-15：中心飞行器 obj106（wing_center）也单独录一步。
#   此前三次使用（41F / 47F / 45F）完全不产生 step，位移被算进下一个移动步，
#   前端只看到英雄凭空瞬移、步骤表里没有任何说明。
for _nm in ('wing_up', 'wing_down', 'wing_center'):
    _o = getattr(M.World, _nm)
    def _mk(o):
        def f(self, *a, **k):
            lg = o(self, *a, **k)
            record(self, None, lg)
            return lg
        return f
    setattr(M.World, _nm, _mk(_o))

# ✅ 2026-11-18（用户：祭坛献祭缺步缺日志）：face_altar 是零位移触发（Java directCheck 面朝祭坛），
#   旧代码不录步 → 4F 献祭的 -18G / DEF 10→14 被算到紧接着的移动步头上，时间轴上根本看不到这次献祭。
#   这里补录一个原地步（d=None 沿用上一朝向），日志即 face_altar 返回的「祭坛献金…」。
_ofa = M.World.face_altar
def face_altar_rec(self, ax, ay):
    lg = _ofa(self, ax, ay)
    txt = ';'.join(lg or [])
    if txt and ('不足' in txt or '错误' in txt or '必须' in txt):
        return lg                     # 失败不记步（与 use_* 口径一致）
    record(self, None, lg, face=(ax, ay))   # ✅ 面朝祭坛格（用户：买完东西要朝向祭坛）
    return lg
M.World.face_altar = face_altar_rec

# ✅ 2026-11-19（用户：#2731 朝右撞盗贼对话）：face_dig 同 face_altar，零位移触发，补录一个原地步。
_odig = M.World.face_dig
def face_dig_rec(self, tx, ty):
    lg = _odig(self, tx, ty)
    txt = ';'.join(lg or [])
    if txt and ('blocked' in txt or '不足' in txt or '错误' in txt or '必须' in txt):
        return lg                     # 失败不记步
    record(self, None, lg, face=(tx, ty))   # ✅ 面朝凿墙/盗贼目标格
    return lg
M.World.face_dig = face_dig_rec

# ✅ 2026-11-19（用户：别踏进 NPC 格再退）：face_talk 同 face_altar/face_dig，零位移触发，补录原地步。
_otalk = M.World.face_talk
def face_talk_rec(self, tx, ty):
    lg = _otalk(self, tx, ty)
    txt = ';'.join(lg or [])
    if txt and ('blocked' in txt or '不足' in txt or '错误' in txt or '必须' in txt):
        return lg
    record(self, None, lg, face=(tx, ty))   # ✅ 面朝交谈 NPC 目标格
    return lg
M.World.face_talk = face_talk_rec

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
                  d=last_dir[0], e='', l='',
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

# ✅ 2026-11-17（用户指出：吸血鬼的伤害角标没显示）：
#   前端 renderDmg() 只遍历 floors[f].objs 里 v[2]=='m' 的格；
#   而 objs 上面只从静态 base_cells() 生成 —— **事件写入的怪全部缺失**，
#   导致「剩余怪伤害」角标不显示（吸血鬼 obj59 是最典型的一处）。
#   实测共 34 处：3F×4 / 20F×1 / 32F×2 / 40F×12 / 42F×5 / 48F×1 / 49F×8。
#   这里把 FLOOR_WRITES 里的 MONSTER 并入 objs（纯展示层，不影响引擎推演）。
_added = 0
for _f, _arr in M.FLOOR_WRITES.items():
    _k = str(_f)
    if _k not in floors:
        continue
    for (_x, _y, _o) in _arr:
        if not _o:
            continue
        if M.TYPE.get(M.oatr(_o, 3)) != 'MONSTER':
            continue
        if _f == 40 and (_x, _y) == (6, 6):
            # ✅ 2026-11-19（用户：40F(6,6) 不用单独显示伤害）：
            #   该格是 66/126 围杀剧本的中转格 —— 13 只怪依次走到这里被逐只击破，
            #   玩家并不上门打这一格，挂「剩余伤害」角标会误导（还会随步数变来变去）。
            continue
        _key = '%d,%d' % (_x, _y)
        if _key in floors[_k]['objs']:
            continue                                  # 静态已有，不覆盖
        floors[_k]['objs'][_key] = [_o, M.oname(_o)[:24], 'm']
        _added += 1
print('=== floors.objs 补入事件写入怪物 %d 处（用于伤害角标）' % _added)

# ✅ 2026-11-18（用户指出：49F/50F 魔王伤害角标缺失）：
#   ゼノ obj57 是剧情事件动态 set_at（49F(6,3) 由 apply_floor_events 写入；
#   50F(6,5) 由小偷对话 12 页 Zeno2 变身写入），不在 base_cells 也不在 FLOOR_WRITES，
#   故上面两轮补入都漏掉。显式补 m，让 renderDmg 画剩余伤害（四维封印后 800/500/100）。
for _fk, _fx, _fy in (('49', 6, 3), ('50', 6, 5)):
    if _fk in floors:
        floors[_fk]['objs']['%d,%d' % (_fx, _fy)] = [57, M.oname(57)[:24], 'm']
print('=== 补入 49F/50F 魔王 obj57 伤害角标 2 处')

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

# ✅ 2026-11-16（用户指出：打完魔龙后原魔龙格未正确显示地面与战利品）：
#   35F 的 3 瓶青薬 obj77 (5,4)(6,4)(7,4) 与雪の結晶 obj110 (6,5) 由 apply_floor_events
#   「进层即写」，dyn 记在首次进 35F 那一步（约 i=3955）；但按原作它们属**魔龙战后补给**
#   （Java MTower.java@2535 条件 [45][58] 清空后才 @2560/2578 摆出）。
#   路线里魔龙要到很晚才打（需 49F 屠龙匕），于是画面上战利品提前近 1900 步出现。
#   这里把这几格的 dyn 步号改到「魔龙击杀步」，与 10F/20F 的战利品口径统一。
_M35 = None
for s in steps:
    if s['f'] == 35 and 'obj74' in s['l'] and '击杀' in s['l']:
        _M35 = s['i']
        break
if _M35 is not None:
    _F35_POST = {(5, 4), (6, 4), (7, 4), (6, 5)}          # 3 瓶青薬 + 雪の結晶
    for _d in dyn['35']:
        if (_d[0], _d[1]) in _F35_POST and _d[2] < _M35:
            _d[2] = _M35                                  # 推迟到魔龙阵亡那一步才出现
    # 同一批格子的 cons（拾取记录）若早于 M35，也一并推到 M35 之后 ——
    #   否则「药还没出现就被消耗」，画面该格会提前变空。
    for _c in cons.get('35', []):
        if (_c[0], _c[1]) in _F35_POST and _c[2] < _M35:
            _c[2] = _M35 + 1
    # ✅ 2026-11-16（用户指出：打完魔龙后原魔龙格未全部显示地面）：
    #   35F 是九宫格巨型 Boss —— 8 个 NORMAL 装饰件 53/54/55/63/64/65/73/75 与魔龙同生共死。
    #   Java MTower.java@2536-2550 在魔龙死后把 (5,6)(7,6)(5,5)(6,5)(7,5)(5,4)(6,4)(7,4) 全清，
    #   但引擎只清了「被踩过」的格 → 其余装饰件一直挂在图上。
    #   这里在魔龙阵亡步给九宫格剩余格补 cons（前端据此贴地板、不再画装饰件）。
    _F35_BODY = [(5, 5), (6, 5), (7, 5), (5, 6), (6, 6), (7, 6), (5, 7), (7, 7)]
    _done35 = {(c[0], c[1]) for c in cons.get('35', [])}
    for (bx, by) in _F35_BODY:
        if (bx, by) not in _done35:
            cons['35'].append([bx, by, _M35, 'f'])

# ✅ 2026-11-18（用户：40F 评分 NPC 在 BOSS 阵亡前就出现）：
#   obj69「この階までのあなたの…評価」评分 NPC 原作里都是 BOSS 死后才立于原位
#   （10F(6,4) dyn 记在击破步 1637、20F(6,4) 在 2834、49F(6,3) 在 5579），
#   但 40F(6,2) 因 mota_core 对 NPC 类事件写入开绿灯（原规则会把静态金騎士挡掉），
#   进层就写进了 over，dyn 也记到了进层步 @3968 —— 画面上一进 40F 就有评分 NPC。
#   这里统一口径：凡评分 NPC 的 dyn 早于本层「★击败」步，一律推迟到击破那一步。
_boss_step = {}
for _s in steps:
    if '★击败' in (_s['l'] or ''):
        _boss_step.setdefault(_s['f'], _s['i'])
_fix69 = 0
for _fk, _arr in dyn.items():
    _bs = _boss_step.get(int(_fk))
    if not _bs:
        continue
    for _d in _arr:
        if _d[3] == 69 and _d[2] < _bs:
            _d[2] = _bs
            _fix69 += 1
if _fix69:
    print('=== 评分 NPC(obj69) 推迟到本层击破步 %d 处' % _fix69)

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

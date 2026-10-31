# -*- coding: utf-8 -*-
"""build_current.py —— 用「当前 segs 路线」（run_segs.py 1F→31F）重建 merged_route.json。

与 build_merged.py（基于旧路线 CSV，7F 暴毙）不同：
  · 本脚本消费 run_segs.py 的逐格 TRACE（已由 mota_core 实算、0 误差验证）；
  · 全部步骤 status='ok'（无 dead/blocked/invalid）；
  · 段标 A=1F-11F / B=12F-20F / C=21F-31F；
  · 额外内嵌 monstats（objid -> [hp,atk,def,name]）供网页显示剩余怪物伤害。

用法：cd 09_TAS推演 && RECORD_TRACE=1 STOP_31F=1 python build_current.py
输出：merged_route.json（覆盖）
"""
import os, sys, json, io, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
import mota_core as M

os.environ['RECORD_TRACE'] = '1'
os.environ['STOP_31F'] = '1'
import run_segs

rc = run_segs.main()
if rc != 0:
    print('!! run_segs.main() rc=%d —— 路线未完整跑到 31F' % rc)
    sys.exit(1)

TRACE = run_segs.TRACE
w = run_segs.LAST_W
print('TRACE 步数:', len(TRACE), ' 终点:', TRACE[-1]['after'])

DIRCH = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', None: '·'}


def seg_of(f):
    return 'A' if f <= 11 else ('B' if f <= 20 else 'C')


def kindof(o):
    if o == 115:
        return 'x'
    t = M.TYPE.get(M.oatr(o, 3))
    return {'MONSTER': 'm', 'DOOR': 'd', 'KEY': 'k', 'ITEM': 'i', 'STATUS': 'i',
            'MESSAGE': 'n', 'SAIDAN': 'a', 'BUY': 's', 'SELL': 's', 'SCORE': 'q'}.get(t, 'x')


def joinlog(s):
    return s.get('log') or ''


# ---------- floors 初始化 ----------
floors = {}
for f in range(1, 32):
    floors[f] = dict(steps=0, loss=0, kills=0, doors=0, pickups=0, visits=0, entry=None,
                     exit=None, terrain=[[M.terrain(f, x, y) for x in range(13)] for y in range(13)],
                     objs={}, path=[], minhp=None, mincell=None, monsters={}, doorcol={},
                     picklist={}, special=[], reached=False, exec_steps=0)

# ---------- 逐步汇总 ----------
prevf = None
for s in TRACE:
    fd = floors[s['floor']]
    fd['steps'] += 1
    fd['reached'] = True
    fd['exec_steps'] += 1
    if fd['entry'] is None:
        fd['entry'] = s['before']
    fd['exit'] = s['after']
    dh = s['after']['hp'] - s['before']['hp']
    if dh < 0:
        fd['loss'] += -dh
    lg = joinlog(s)
    if '击杀' in lg:
        fd['kills'] += 1
        for part in lg.split('击杀')[1:]:
            name = part.strip().split(' ')[1] if len(part.strip().split(' ')) > 1 else '?'
            fd['monsters'][name] = fd['monsters'].get(name, 0) + 1
    if '门 obj' in lg and '开' in lg:
        fd['doors'] += 1
        for col, cn in (('黄门', '黄'), ('蓝门', '蓝'), ('红门', '红')):
            if col in lg:
                fd['doorcol'][cn] = fd['doorcol'].get(cn, 0) + 1
    if '拾' in lg:
        fd['pickups'] += 1
    for key, label in (('祭坛', '祭坛献金'), ('购物', '商店'), ('飞行之珠', '飞行之珠传送'),
                       ('撞塌暗墙', '暗墙'), ('盗賊', '盗贼凿墙'), ('★', '关键事件')):
        if key in lg:
            fd['special'].append('%s@%dF(%d,%d)' % (label, s['floor'], s['x'], s['y']))
    if fd['minhp'] is None or s['after']['hp'] < fd['minhp']:
        fd['minhp'] = s['after']['hp']
        fd['mincell'] = [s['floor'], s['x'], s['y']]
    if prevf != s['floor']:
        fd['visits'] += 1
        prevf = s['floor']
    fd['path'].append([s['x'], s['y']])

# ---------- objs / path 收尾 ----------
for f in range(1, 32):
    for y in range(13):
        for x in range(13):
            o = M.obj_raw(f, x, y)
            if o:
                floors[f]['objs']['%d,%d' % (x, y)] = [o, M.oname(o)[:16], kindof(o)]
    p = floors[f]['path']
    q = []
    for c in p:
        if not q or q[-1] != c:
            q.append(c)
    floors[f]['path'] = q
    floors[f]['special'] = sorted(set(floors[f]['special']))

# ---------- csteps（扁平化） ----------
csteps = []
for k, s in enumerate(TRACE):
    o = dict(i=k + 1, s=seg_of(s['floor']), f=s['floor'], x=s['x'], y=s['y'],
             d=DIRCH.get(s['dir'], '·'), e='', l=joinlog(s),
             hp=s['after']['hp'], a=s['after']['atk'], df=s['after']['dfn'],
             g=s['after']['gold'], ky=s['after']['ky'], kb=s['after']['kb'],
             kr=s['after']['kr'], dh=s['after']['hp'] - s['before']['hp'],
             da=s['after']['atk'] - s['before']['atk'],
             dd=s['after']['dfn'] - s['before']['dfn'],
             dg=s['after']['gold'] - s['before']['gold'],
             st='ok')
    csteps.append(o)

# ---------- cons（已消耗格） ----------
cons = collections.OrderedDict()
for k, s in enumerate(TRACE):
    pf = s['floor']
    for (cf, cxx, cyy) in s['cl']:
        a = k if pf == cf else max(k - 1, 0)
        if M.terrain(cf, cxx, cyy) == 2:
            kind = 'u' if M.stair_up(cf, cxx, cyy) else 'd'
        else:
            kind = 'f'
        cons.setdefault(str(cf), []).append([cxx, cyy, a, kind])

# ---------- markers：2F 栅栏门（本路线未开，攻略 §7.1 要求救小偷）----------
GATE_CELLS = [(5, 5), (9, 5), (5, 8), (9, 8), (5, 11), (9, 11)]
LOOT_CELLS = [(3, 10), (4, 10), (3, 11)]
KEY_CELLS = [(3, 4), (4, 4), (3, 5)]
markers = collections.OrderedDict()
markers['2'] = ([dict(x=x, y=y, t='gate', label='栅栏门(未开)') for x, y in GATE_CELLS]
                + [dict(x=x, y=y, t='loot', label='蓝药(门后未取)') for x, y in LOOT_CELLS]
                + [dict(x=x, y=y, t='loot', label='钥匙(门后未取)') for x, y in KEY_CELLS])
# 攻略 §7.1 明文的 2F 救小偷前置链缺失提示
markers['2'].append(dict(x=11, y=11, t='death',
                         label='⚠ 2F 小偷 obj88 未救（攻略 §7.1：过35F必须救2F小偷）'))
markers['35'] = [dict(x=5, y=10, t='death',
                      label='⚠ 35F 盗贼须先救 2F 小偷（本路线未做前置链）')]

# ---------- monstats：怪物属性表（供网页显示伤害） ----------
monstats = {}
for o in range(len(M.OA)):
    if M.TYPE.get(M.oatr(o, 3)) == 'MONSTER':
        monstats[str(o)] = [M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), M.oname(o)[:16]]

# ---------- 汇总 ----------
tot = dict(steps=len(csteps), loss=sum(floors[f]['loss'] for f in range(1, 32)),
           kills=sum(floors[f]['kills'] for f in range(1, 32)),
           doors=sum(floors[f]['doors'] for f in range(1, 32)),
           pickups=sum(floors[f]['pickups'] for f in range(1, 32)))
minhp = min((s['after']['hp'], s['floor'], s['x'], s['y'], k + 1)
            for k, s in enumerate(TRACE))

segs = collections.OrderedDict()
for k, s in enumerate(TRACE):
    g = segs.setdefault(seg_of(s['floor']), dict(steps=0, loss=0, kills=0, doors=0, pickups=0,
                                                 first=k + 1, last=k + 1, mism=0, executed=0))
    g['steps'] += 1
    g['last'] = k + 1
    g['executed'] += 1
    if s['after']['hp'] - s['before']['hp'] < 0:
        g['loss'] += -(s['after']['hp'] - s['before']['hp'])

steps_ab = sum(1 for s in TRACE if seg_of(s['floor']) in ('A', 'B'))
steps_c = sum(1 for s in TRACE if seg_of(s['floor']) == 'C')

out = dict(total=tot, segs=segs, floors=floors, steps=csteps, issues=[],
           final=TRACE[-1]['after'], minhp=minhp, markers=markers, dead=None, blocked=None,
           verify=dict(rows_ab=steps_ab, steps_ab=steps_ab, steps_c=steps_c,
                       gate_rows=18, gate_cells=6, dead_line=None, hp_drift=0),
           monstats=monstats)
out['cons'] = cons

json.dump(out, io.open(DED + 'merged_route.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('written merged_route.json')
print('  steps', len(csteps), 'loss', tot['loss'], 'kills', tot['kills'], 'final', out['final'])
print('  segs', {k: v['steps'] for k, v in segs.items()})

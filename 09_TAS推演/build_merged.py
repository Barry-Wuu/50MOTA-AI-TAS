# -*- coding: utf-8 -*-
"""把 1F→31F 路线用「修正后的 mota_core」重放，并如实记录 2F 栅栏门问题。

修正要点（源码 / np2kai 实测 / 仓库笔记三方交叉验证）：
  · 2F 六个 obj19 是监狱栅栏门，在 (6,2)(8,2) 两只門番Ｂ清空前不可通行；
  · 两只門番Ｂ 属性 HP100/ATK180/DEF110，1F→21F 全程英雄最高 ATK115，永远打不动，
    故本段内栅栏门永远打不开；
  · 原录制路线 43..60 行靠穿栅栏门去捡 3 瓶青い回復薬(+600HP)，属非法；
    合法越狱只能走盗贼挖的洞 2F(2,7)（3F 剧本已把该墙挖通）。

因此本脚本：
  · 43..60 行标记 invalid（未执行）；
  · 61..67 行即合法越狱路径；
  · 之后逐行实算，记录实际 HP 与录制 HP 的漂移；
  · 遇到「打不过」即标记 dead，其后全部标记 unreachable。
"""
import sys, json, csv, io, collections

TOOLS = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools'
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
DED = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/'
sys.path.insert(0, TOOLS)
import mota_core as M

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRCH = {(1, 0): '→', (-1, 0): '←', (0, 1): '↓', (0, -1): '↑', None: '·'}
FAIL_PREFIX = ('blocked', '打不动', '无', '买不起', '熔岩烫死', '打不过')
GATE_ROWS = set(range(43, 61))          # 1-based 43..60：原路线穿 2F 栅栏门的违规绕路
GATE_CELLS = [(5, 5), (9, 5), (5, 8), (9, 8), (5, 11), (9, 11)]
LOOT_CELLS = [(3, 10), (4, 10), (3, 11)]   # 3 瓶青い回復薬，栅栏门后
KEY_CELLS = [(3, 4), (4, 4), (3, 5)]       # 3 把扉の鍵，同样在门后


def snap(h):
    return dict(hp=h.hp, atk=h.atk, dfn=h.dfn, gold=h.gold,
                ky=h.keys.get('y', 0), kb=h.keys.get('b', 0), kr=h.keys.get('r', 0),
                items=sorted(h.items))


def delta(a, b):
    return dict(hp=b['hp'] - a['hp'], atk=b['atk'] - a['atk'], dfn=b['dfn'] - a['dfn'],
                gold=b['gold'] - a['gold'], ky=b['ky'] - a['ky'],
                kb=b['kb'] - a['kb'], kr=b['kr'] - a['kr'])


def joinlog(lg):
    return ' ｜ '.join(x for x in (lg or []) if x)


w = M.World.new()
prev = snap(w.hero)
steps = []
issues = []
dead = None
blocked = None


def pick_move(r):
    """按目标格 + 非 HP 状态选方向（HP 已因 2F 少 600 而漂移，不能用它判别）。"""
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    rec = dict(atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))
    h = w.hero
    same = (h.f, h.x, h.y) == (tf, tx, ty)
    best = None
    for d in DIRS:
        c = w.clone()
        lg = c.move(*d)
        if lg and lg[0].startswith(FAIL_PREFIX):
            continue
        hh = c.hero
        sc = 0
        if (hh.f, hh.x, hh.y) == (tf, tx, ty):
            sc += 8
        elif same and (hh.f, hh.x, hh.y) == (h.f, h.x, h.y) and lg:
            sc += 4
        else:
            continue
        for k, cur in (('atk', hh.atk), ('dfn', hh.dfn), ('gold', hh.gold)):
            if cur == rec[k]:
                sc += 1
        for k, kk in (('ky', 'y'), ('kb', 'b'), ('kr', 'r')):
            if hh.keys.get(kk, 0) == rec[k]:
                sc += 1
        if bool(lg) == bool((r['event'] or '').strip()):
            sc += 1
        if best is None or sc > best[0]:
            best = (sc, d, c, lg)
    return best


# ---------------------------------------------------------------------------
# 段 A/B：1F→21F 录制 CSV
# ---------------------------------------------------------------------------
rows_m = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8')))
LAST_CLEARED = set(w.cleared)


def push(seg, line, recstep, floor, x, y, d, event, log, status, rec=None, mism=None, pos=None):
    global prev, LAST_CLEARED
    after = snap(w.hero)
    new_cl = sorted(w.cleared - LAST_CLEARED)
    LAST_CLEARED = set(w.cleared)
    steps.append(dict(seg=seg, line=line, recstep=recstep, floor=floor, x=x, y=y, dir=d,
                      dch=DIRCH.get(d, '·'), event=event, log=log, before=prev, after=after,
                      d=delta(prev, after), rec=rec, mism=mism or [], status=status,
                      pos=pos or [w.hero.f, w.hero.x, w.hero.y], cl=new_cl))
    prev = after


for i, r in enumerate(rows_m):
    line = i + 1
    tf, tx, ty = int(r['floor']), int(r['x']), int(r['y'])
    ev = (r['event'] or '').strip()
    rec = dict(hp=int(r['hp']), atk=int(r['atk']), dfn=int(r['def']), gold=int(r['gold']),
               ky=int(r['ky']), kb=int(r['kb']), kr=int(r['kr']))

    if dead or blocked:
        push('A' if line <= 1243 else 'B', line, int(r['step']), tf, tx, ty, None,
             ev, '未执行（前段已无法继续）', 'unreachable', rec)
        continue

    if line in GATE_ROWS:
        push('A', line, int(r['step']), tf, tx, ty, None,
             (ev + ' ' if ev else '') + '（穿越 2F 监狱栅栏门 obj19，违规）',
             '❌ 未执行：栅栏门未开（须先击败 (6,2)(8,2) 两只門番Ｂ）',
             'invalid', rec)
        continue

    best = pick_move(r)
    if best is None:
        # 说明这一步引擎走不通（多半是 HP 不足 / 缺钥匙）
        h = w.hero
        reason = '无法执行'
        lg = ''
        for d in DIRS:
            c = w.clone()
            l2 = c.move(*d)
            if l2 and l2[0].startswith('打不过'):
                lg = l2[0]; reason = 'HP 不足，打不过'
                break
            if l2 and l2[0].startswith('无') and l2[0].find('钥匙') >= 0:
                lg = l2[0]; reason = '缺钥匙'
                break
            if l2 and l2[0].startswith('blocked'):
                lg = l2[0]; reason = '被阻挡'
        if reason == 'HP 不足，打不过':
            import re as _re
            _m = _re.search(r'需掉血\s*(\d+)', lg or '')
            dead = dict(line=line, floor=tf, x=tx, y=ty, event=ev, log=lg,
                        hp=h.hp, recorded_hp=int(r['hp']),
                        need=(int(_m.group(1)) if _m else None))
            push('A' if line <= 1243 else 'B', line, int(r['step']), tf, tx, ty, None,
                 ev, '💀 ' + (lg or reason), 'dead', rec, mism=[lg or reason])
            issues.append(dict(kind='dead', line=line, floor=tf, x=tx, y=ty,
                               msg='路线在此暴毙：%s（当前 HP%d，录制 HP%d）。根因是 2F 三瓶蓝药(+600HP)'
                                   '因栅栏门未开而不可得，HP 全程比原计划少 600。'
                                   % (lg or reason, h.hp, int(r['hp']))))
        else:
            blocked = dict(line=line, floor=tf, x=tx, y=ty, event=ev, log=lg, reason=reason)
            push('A' if line <= 1243 else 'B', line, int(r['step']), tf, tx, ty, None,
                 ev, '❌ ' + (lg or reason), 'blocked', rec, mism=[lg or reason])
            issues.append(dict(kind='blocked', line=line, floor=tf, x=tx, y=ty,
                               msg='%s：%s' % (reason, lg or '（无日志）')))
        continue

    sc, d, c, lg = best
    w = c
    hh = w.hero
    mism = []
    if hh.hp != rec['hp']:
        mism.append('HP 记录%d 实算%d（差%+d）' % (rec['hp'], hh.hp, hh.hp - rec['hp']))
    if (hh.f, hh.x, hh.y) != (tf, tx, ty):
        mism.append('落点 %dF(%d,%d)' % (hh.f, hh.x, hh.y))
    push('A' if line <= 1243 else 'B', line, int(r['step']), tf, tx, ty, d,
         ev, joinlog(lg), 'ok', rec, mism)

# ---------------------------------------------------------------------------
# 2F 栅栏门问题总账（作为独立 issue，便于在问题清单里点开）
# ---------------------------------------------------------------------------
issues.append(dict(kind='gate', line=43, floor=2, x=5, y=8,
                   msg='2F 监狱栅栏门 obj19 未开。两只門番Ｂ (6,2)(8,2) 属性 HP100/ATK180/DEF110，'
                       '1F→21F 全程英雄最高 ATK115，永远打不动，故门永不打开。'
                       '原路线第 43–60 行靠穿栅栏门去捡 3 瓶青い回復薬(+600HP)，属非法，已全部作废；'
                       '合法越狱只能走盗贼挖开的洞 2F(2,7)。'))
issues.append(dict(kind='gate', line=1405, floor=2, x=5, y=8,
                   msg='回程第 1405/1410/1418/1423 行同样要穿 2F 栅栏门；'
                       '且门后 3 把扉の鍵 (3,4)(4,4)(3,5) 同样不可得。'
                       '（本段已在此前的 7F 暴毙，回程整段未执行。）'))

# ---------------------------------------------------------------------------
# 段 C：21F→31F（前段已死则全部 unreachable，仅保留计划路径供地图显示）
# ---------------------------------------------------------------------------
rows_c = list(csv.DictReader(io.open(DED + '魔塔1_route_21F到30F_原版.csv', encoding='utf-8-sig')))
cur_line = len(rows_m) + 1
for r in rows_c:
    tf, tx, ty = int(r['楼层']), int(r['x']), int(r['y'])
    ev = (r['动作'] or '').strip()
    note = (r['说明'] or '').strip()
    if note:
        ev += '：' + note
    push('C', cur_line, None, tf, tx, ty, None, ev, '未执行（前段已无法继续）', 'unreachable')
    cur_line += 1

# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
floors = {}
for f in range(1, 32):
    floors[f] = dict(steps=0, loss=0, kills=0, doors=0, pickups=0, visits=0, entry=None,
                     exit=None, terrain=[[M.terrain(f, x, y) for x in range(13)] for y in range(13)],
                     objs={}, path=[], minhp=None, mincell=None, monsters={}, doorcol={},
                     picklist={}, special=[], reached=False, exec_steps=0)

prevf = None
for s in steps:
    fd = floors[s['floor']]
    fd['steps'] += 1
    if s['status'] in ('ok', 'dead', 'note'):
        fd['reached'] = True
        fd['exec_steps'] += 1
    if fd['entry'] is None:
        fd['entry'] = s['before']
    fd['exit'] = s['after']
    if s['d']['hp'] < 0:
        fd['loss'] += -s['d']['hp']
    lg = s['log']
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
        if key in lg or key in s['event']:
            fd['special'].append('%s@%dF(%d,%d)' % (label, s['floor'], s['x'], s['y']))
    if s['status'] in ('ok', 'dead', 'note') and s['after']['hp'] is not None:
        if fd['minhp'] is None or s['after']['hp'] < fd['minhp']:
            fd['minhp'] = s['after']['hp']
            fd['mincell'] = [s['floor'], s['x'], s['y']]
    if prevf != s['floor']:
        fd['visits'] += 1
        prevf = s['floor']
    fd['path'].append([s['x'], s['y']])


def kindof(o):
    if o == 115:
        return 'x'
    t = M.TYPE.get(M.oatr(o, 3))
    return {'MONSTER': 'm', 'DOOR': 'd', 'KEY': 'k', 'ITEM': 'i', 'STATUS': 'i',
            'MESSAGE': 'n', 'SAIDAN': 'a', 'BUY': 's', 'SELL': 's', 'SCORE': 'q'}.get(t, 'x')


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

# 已消耗格：只统计真正执行过的步
cons = collections.OrderedDict()
for k, s in enumerate(steps):
    if s['status'] not in ('ok', 'dead', 'note'):
        continue
    pf = (s.get('pos') or [s['floor']])[0]
    for (cf, cxx, cyy) in (s.get('cl') or []):
        a = k if pf == cf else max(k - 1, 0)
        if M.terrain(cf, cxx, cyy) == 2:
            kind = 'u' if M.stair_up(cf, cxx, cyy) else 'd'
        else:
            kind = 'f'
        cons.setdefault(str(cf), []).append([cxx, cyy, a, kind])

# 2F 特殊标记：栅栏门 / 门后战利品
markers = collections.OrderedDict()
markers['2'] = ([dict(x=x, y=y, t='gate', label='栅栏门(未开)') for x, y in GATE_CELLS]
                + [dict(x=x, y=y, t='loot', label='蓝药(不可得)') for x, y in LOOT_CELLS]
                + [dict(x=x, y=y, t='loot', label='钥匙(不可得)') for x, y in KEY_CELLS])
if dead:
    markers.setdefault(str(dead['floor']), []).append(
        dict(x=dead['x'], y=dead['y'], t='death', label='暴毙点'))

# 压缩步记录
csteps = []
for s in steps:
    o = dict(i=s['line'], s=s['seg'], f=s['floor'], x=s['x'], y=s['y'], d=s['dch'],
             e=s['event'], l=s['log'], hp=s['after']['hp'], a=s['after']['atk'],
             df=s['after']['dfn'], g=s['after']['gold'], ky=s['after']['ky'],
             kb=s['after']['kb'], kr=s['after']['kr'], dh=s['d']['hp'],
             da=s['d']['atk'], dd=s['d']['dfn'], dg=s['d']['gold'], st=s['status'])
    if s.get('recstep'):
        o['rs'] = s['recstep']
    if s.get('rec'):
        o['rhp'] = s['rec']['hp']
    if s['mism']:
        o['mm'] = s['mism']
    p = s.get('pos')
    if p and [p[0], p[1], p[2]] != [s['floor'], s['x'], s['y']]:
        o['p'] = p
    csteps.append(o)

tot = dict(steps=len(steps), loss=sum(floors[f]['loss'] for f in range(1, 32)),
           kills=sum(floors[f]['kills'] for f in range(1, 32)),
           doors=sum(floors[f]['doors'] for f in range(1, 32)),
           pickups=sum(floors[f]['pickups'] for f in range(1, 32)))
minhp = min((s['after']['hp'], s['floor'], s['x'], s['y'], s['line'])
            for s in steps if s['status'] in ('ok', 'dead', 'note'))

segs = collections.OrderedDict()
for s in steps:
    g = segs.setdefault(s['seg'], dict(steps=0, loss=0, kills=0, doors=0, pickups=0,
                                       first=s['line'], last=s['line'], mism=0, executed=0))
    g['steps'] += 1
    g['last'] = s['line']
    if s['status'] in ('ok', 'dead', 'note'):
        g['executed'] += 1
    if s['mism']:
        g['mism'] += 1
    if s['d']['hp'] < 0:
        g['loss'] += -s['d']['hp']

out = dict(total=tot, segs=segs, floors=floors, steps=csteps, issues=issues,
           final=snap(w.hero), minhp=minhp, markers=markers, dead=dead, blocked=blocked,
           verify=dict(rows_ab=len(rows_m), steps_ab=sum(1 for s in steps if s['seg'] in ('A', 'B')),
                       steps_c=sum(1 for s in steps if s['seg'] == 'C'),
                       gate_rows=len(GATE_ROWS), gate_cells=len(GATE_CELLS),
                       dead_line=(dead['line'] if dead else None),
                       hp_drift=(dead['hp'] - dead['recorded_hp'] if dead else 0)))
out['cons'] = cons

json.dump(out, io.open(DED + 'merged_route.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('steps', len(steps), 'loss', tot['loss'], 'kills', tot['kills'])
print('final', snap(w.hero))
print('dead', dead)
print('blocked', blocked)
print('minhp', minhp)
print('issues', len(issues))
for it in issues:
    print('  ', it['kind'], 'line', it['line'], it['msg'][:90])
print('cons cells', sum(len(v) for v in cons.values()))

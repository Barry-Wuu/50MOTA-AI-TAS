# -*- coding: utf-8 -*-
"""完整 1F→11F 合法路线：trap_escape + manual PLAN(→8F) + plan2(8F→11F)，整段重放校验。
   产出：魔塔1_route_1F到11F_合法_v2.csv（含逐格/事件/状态）。"""
import sys, time, csv, io
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import manual
import route_build as RB

# ---- 记录 manual PLAN 的动作 ----
moves = list(manual.PREAMBLE_MOVES)          # 前奏：plan2(avoid) 1F→3F + 触发扒装 + 越狱
_orig = manual.W.move
def rec(dx, dy):
    lg = _orig(dx, dy)
    moves.append((dx, dy))
    return lg
manual.W.move = rec
print('起点(manual): %dF(%d,%d) HP%d A%d D%d G%d' % (manual.W.hero.f, manual.W.hero.x, manual.W.hero.y,
      manual.W.hero.hp, manual.W.hero.atk, manual.W.hero.dfn, manual.W.hero.gold))
manual.execute(verbose=False)
h = manual.W.hero
print('PLAN 后: %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d 步%d' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
      h.keys['y'], h.keys['b'], h.keys['r'], len(moves)))

# ---- 先保存已验证的 1F→9F 合法段（trap_escape + PLAN）----
def dump_csv(moves, out):
    wc = M.World.new()
    rows = [dict(step=0, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
                 atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
                 ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
                 event='', dir='')]
    for i, (dx, dy) in enumerate(moves):
        lg = wc.move(dx, dy)
        rows.append(dict(step=i + 1, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
                         atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
                         ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
                         event=';'.join(lg)[:80], dir='%d,%d' % (dx, dy)))
    with io.open(out, 'w', encoding='utf-8-sig', newline='') as fp:
        w2 = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w2.writeheader(); w2.writerows(rows)
    return len(rows)

n9 = dump_csv(moves, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_1F到9F_合法.csv')
print('已存 1F→9F 合法段（%d 行）' % n9)

# ---- plan2 从 8F(6,2) 到 11F ----
t = time.time()
r = RB.plan2(lambda f, x, y: f == 11, start=manual.W, goal_cell=(11, 6, 10), max_states=2000000)
dt = time.time() - t
if not r or (isinstance(r, tuple) and r[0] == 'cap'):
    print('8F→11F 失败:', r if not r else ('CAP %s' % r[1]), '(%.1fs)' % dt)
    sys.exit(1)
w, p2moves = r
moves.extend(p2moves)
h = w.hero
print('8F→11F OK 步+%d (%.1fs) → 终态 %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d' % (
    len(p2moves), dt, h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

# ---- 整段重放校验 ----
print('总步数 %d' % len(moves))
wv = M.World.new()
fails = []
for i, (dx, dy) in enumerate(moves):
    lg = wv.move(dx, dy)
    if lg and lg[0].startswith(('blocked', '打不动', '打不过', '无黄', '无蓝', '无红', '买不起')):
        fails.append((i, lg[:1]))
        break
hv = wv.hero
if fails:
    print('❌ 重放卡在 step %d: %s' % fails[0])
else:
    print('✅ 重放 0 误差，终态 %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d' % (
        hv.f, hv.x, hv.y, hv.hp, hv.atk, hv.dfn, hv.gold, hv.keys['y'], hv.keys['b'], hv.keys['r']))
    # 存 CSV
    out = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/魔塔1_route_1F到11F_合法_v2.csv'
    # 重新放一遍生成逐行记录
    wc = M.World.new()
    rows = []
    rows.append(dict(step=0, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
                     atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
                     ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
                     event='', dir=''))
    for i, (dx, dy) in enumerate(moves):
        lg = wc.move(dx, dy)
        rows.append(dict(step=i+1, floor=wc.hero.f, x=wc.hero.x, y=wc.hero.y, hp=wc.hero.hp,
                         atk=wc.hero.atk, dfn=wc.hero.dfn, gold=wc.hero.gold,
                         ky=wc.hero.keys['y'], kb=wc.hero.keys['b'], kr=wc.hero.keys['r'],
                         event=';'.join(lg)[:80], dir='%d,%d' % (dx, dy)))
    with io.open(out, 'w', encoding='utf-8-sig', newline='') as fp:
        w2 = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w2.writeheader(); w2.writerows(rows)
    print('已存 %s（%d 行）' % (out, len(rows)))

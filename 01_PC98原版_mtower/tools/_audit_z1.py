# -*- coding: utf-8 -*-
"""1区（1-10F）血瓶覆盖审计 v2：
- 枚举 1-10F 所有药水瓶（type∈STATUS/ITEM 且 a[10]>0）
- 跑 run_segs.main()，记录每次药水拾取的【目标格】(f,nx,ny)
- 首次进 11F 之前的拾取 = 进11F 前已收集；其余 = 未收集（潜在提升空间）
"""
import sys, os, json, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mota_core as mc
import run_segs

d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'magic_tower1_map_50f.json'), encoding='utf-8'))
OA, TYPE = mc.OA, mc.TYPE

# ---- 1) 枚举 1-10F 所有药水瓶 ----
potions = {}
for fl in range(1, 11):
    f = d[str(fl)]
    obj = f['objects']
    for y in range(len(obj)):
        for x in range(len(obj[y])):
            o = obj[y][x]
            if not o:
                continue
            t = TYPE.get(OA[o][3] if o < len(OA) else 0, '?')
            hp = OA[o][10] if o < len(OA) else 0
            if t in ('STATUS', 'ITEM') and hp:
                potions.setdefault(fl, []).append((x, y, o, hp, mc.oname(o)))

total_hp = sum(v[3] for vv in potions.values() for v in vv)
print('=== 1-10F 药水瓶枚举 ===')
for fl in sorted(potions):
    for (x, y, o, hp, nm) in sorted(potions[fl], key=lambda z: (z[1], z[0])):
        print(f'  {fl}F({x},{y}) obj{o} HP+{hp}')
print(f'  合计 {sum(len(v) for v in potions.values())} 瓶 / {total_hp} HP')

# ---- 2) monkeypatch：记录目标格，首次进 11F 截断 ----
first_11 = [None]
collected = []      # 进11F 前已收集的药水（目标格）
_last_dest = [None] # (f,nx,ny)

_orig_move = mc.World.move
def _move(self, dx, dy):
    h = self.hero
    _last_dest[0] = (h.f, h.x + dx, h.y + dy)
    r = _orig_move(self, dx, dy)
    if first_11[0] is None and self.hero.f == 11:
        first_11[0] = True
    return r
mc.World.move = _move

_orig_pick = mc.World.pick
def _pick2(self, o, log):
    h = self.hero
    if first_11[0] is None:
        hp = OA[o][10] if o < len(OA) else 0
        if hp and TYPE.get(OA[o][3] if o < len(OA) else 0, '?') in ('STATUS', 'ITEM'):
            fd, xd, yd = _last_dest[0] if _last_dest[0] else (h.f, h.x, h.y)
            collected.append((fd, xd, yd, o, hp, mc.oname(o)))
    return _orig_pick(self, o, log)
mc.World.pick = _pick2

print('\n=== 跑 run_segs.main()（截断记录在进11F）===')
with contextlib.redirect_stdout(io.StringIO()) as buf:
    rc = run_segs.main()
print(f'main() 返回 {rc}')
out = buf.getvalue()
for line in out.splitlines():
    if '进 11F' in line or '第一区完成' in line:
        print('  ', line.strip())

print('\n=== 进11F 前已收集药水（共 %d 瓶 / %d HP）===' % (len(collected), sum(c[3] for c in collected)))
for (f, x, y, o, hp, nm) in collected:
    print(f'  {f}F({x},{y}) obj{o} HP+{hp}')

# ---- 3) 未收集 = 枚举 - 已收集 ----
coll_keys = set((f, x, y) for (f, x, y, o, hp, nm) in collected)
print('\n=== 进11F 前未收集的 1-10F 药水瓶（潜在提升空间）===')
un = []
for fl in sorted(potions):
    for (x, y, o, hp, nm) in sorted(potions[fl], key=lambda z: (z[1], z[0])):
        if (fl, x, y) not in coll_keys:
            un.append((fl, x, y, o, hp, nm))
            print(f'  {fl}F({x},{y}) obj{o} HP+{hp}')
print(f'  未收集 {len(un)} 瓶 / {sum(u[3] for u in un)} HP')

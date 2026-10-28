# -*- coding: utf-8 -*-
"""从 17F 断点续跑到 38F（拿骑士盾）。

与旧版的关键差别：**寻路代价里给门加惩罚**，逼 A* 绕门而不是随手开。
  黄门 +60 / 蓝门 +8000 / 红门 +40000（1 步本身仍算 1）
这样「绕 20 步」永远比「开 1 道蓝门」便宜，钥匙账才不会崩。
"""
import sys, csv, heapq, pickle, os
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

DIRS = [(0, -1, '8'), (1, 0, '6'), (0, 1, '2'), (-1, 0, '4')]
DOOR_PEN = {'开黄门': 60, '开蓝门': 8000, '开红门': 40000}
LOG = []


def st(h):
    return '%2dF(%2d,%2d) HP%-5d ATK%2d DEF%2d G%-4d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


def blockers_of(f):
    s = set()
    for y in range(1, 12):
        for x in range(1, 12):
            o = M.obj_raw(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3))
            if ty in ('DOOR', 'MONSTER') or o in M.SHOP:
                s.add((x, y))
    return s


_BLK = {}


def _key(w):
    h = w.hero
    if h.f not in _BLK:
        _BLK[h.f] = blockers_of(h.f)
    blk = _BLK[h.f]
    n = sum(1 for c in w.cleared if c[0] == h.f and (c[1], c[2]) in blk)
    bo = len([c for c in w.bought if c[0] == h.f])
    return (h.f, h.x, h.y, h.keys['y'], h.keys['b'], h.keys['r'],
            h.atk, h.dfn, h.hp // 50, n, bo)


def walk(w, tgt, max_exp=400000):
    if isinstance(tgt, int):
        done = lambda x: x.hero.f == tgt
        heur = lambda x: 30 * abs(x.hero.f - tgt)
    elif callable(tgt):
        done, heur = tgt, lambda x: 0
    else:
        tf, tx, ty = tgt
        done = lambda x: (x.hero.f, x.hero.x, x.hero.y) == tgt
        heur = lambda x: 30 * abs(x.hero.f - tf) + (
            abs(x.hero.x - tx) + abs(x.hero.y - ty) if x.hero.f == tf else 0)
    if done(w):
        return w, []
    seen = {_key(w)}
    cnt = 0
    heap = [(heur(w), 0, 0, w, [])]
    n = 0
    while heap:
        _, _, g, cur, path = heapq.heappop(heap)
        n += 1
        if n > max_exp:
            return None, '展开超限 %d' % n
        for dx, dy, lab in DIRS:
            w2 = cur.clone()
            lg = w2.move(dx, dy)
            if M.blocked(lg):
                continue
            if w2.hero.hp <= 0:
                continue
            k = _key(w2)
            if k in seen:
                continue
            seen.add(k)
            p = path + [(dx, dy, lab, lg)]
            if done(w2):
                return w2, p
            loss = max(0, cur.hero.hp - w2.hero.hp)
            step = 1 + loss // 20
            joined = ' '.join(lg)
            for tag, pen in DOOR_PEN.items():
                if tag in joined:
                    step += pen
                    break
            cnt += 1
            heapq.heappush(heap, (heur(w2) + g + step, cnt, g + step, w2, p))
    return None, '不可达'


def go(tag, w, tgt, max_exp=400000):
    w2, path = walk(w, tgt, max_exp)
    if w2 is None:
        print('  ✗ %-26s %s  [%s]' % (tag, path, st(w.hero)))
        return w, False
    cur = w
    for (dx, dy, lab, lg) in path:
        cur = cur.clone()
        lg = cur.move(dx, dy)
        h = cur.hero
        LOG.append((len(LOG) + 1, h.f, h.x, h.y, lab, ' '.join(lg),
                    h.hp, h.atk, h.dfn, h.gold,
                    h.keys['y'], h.keys['b'], h.keys['r']))
    print('  ✓ %-26s → %-46s [%2d 步]' % (tag, st(w2.hero), len(path)))
    return w2, True


GOALS = [
    # (标签, 目标)  目标 = (层,x,y) / 层号 / 谓词
    ('18F 蓝钥匙 (11,3)', (18, 11, 3)),
    ('18F → 19F', 19),
    ('19F 十字架 (6,3)', (19, 6, 3)),
    ('19F → 20F', 20),
    ('20F 红门后 BOSS (6,6)', (20, 6, 6)),
    ('20F → 21F', 21),
    ('21F → 29F', 29),
    ('29F 下 28F 再上（开暗墙）', (28, 2, 11)),
    ('28F → 29F', 29),
    ('29F → 30F', 30),
    ('30F 封印 (6,6)', (30, 6, 6)),
    ('30F → 31F', 31),
    ('31F → 32F', 32),
    ('32F → 33F', 33),
    ('33F → 34F', 34),
    ('34F → 35F', 35),
    ('35F → 36F', 36),
    ('36F → 37F', 37),
    ('37F 红钥匙 (7,5)', (37, 7, 5)),
    ('37F → 38F', 38),
    ('★38F 骑士盾 (2,7)', (38, 2, 7)),
    ('38F → 39F', 39),
]


def main():
    with open(r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools/ck_17.pkl', 'rb') as fp:
        w = pickle.load(fp)
    print('起点  ' + st(w.hero))
    fails = []
    for tag, tgt in GOALS:
        w, ok = go(tag, w, tgt)
        if not ok:
            fails.append(tag)
            break
    print()
    print('终态  ' + st(w.hero))
    if fails:
        print('断点：', fails)
    out = r'D:/B++/WorkBuddy/mota_tas_tmp2/魔塔1_route_18F到39F.csv'
    with open(out, 'w', newline='', encoding='utf-8-sig') as fp:
        cw = csv.writer(fp)
        cw.writerow(['step', 'floor', 'x', 'y', 'key', 'event',
                     'hp', 'atk', 'def', 'gold', 'ky', 'kb', 'kr'])
        cw.writerows(LOG)
    print('已写 %s（%d 步）' % (out, len(LOG)))
    with open(r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools/ck_38.pkl', 'wb') as fp:
        pickle.dump(w, fp)


if __name__ == '__main__':
    main()

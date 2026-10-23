import json, re, collections

A = '/workspace/f8fd4af0-b7d8-470f-bd1e-d5a9802c97d1/work/.artifacts'
L = [l.rstrip() for l in open(A + '/mtower.jvm', encoding='utf8', errors='replace')]
live = json.load(open(A + '/crops/live.json'))
mp, mo, ma, oa = live['map'], live['mapObject'], live['mapAttribute'], live['objectAttribute']
SMX = json.load(open(A + '/javamap.json'))['strMessage']['1']
INS = re.compile(r'^\s+(\d+): (\w+)\s*(.*?)\s*$')
hd = [(i, l) for i, l in enumerate(L)
      if re.match(r'^  (?:public |private |protected |static |final |synchronized )*[A-Za-z_$][\w\.\$<>\[\]]* [A-Za-z_$][\w<>]*\(.*\);\s*$', l)]


def at(i):
    m = INS.match(L[i]); return (m.group(2), m.group(3)) if m else (None, '')


def num(i):
    op, arg = at(i)
    if op in ('bipush', 'sipush'): return int(arg)
    if op == 'iconst_m1': return -1
    if op and re.match(r'iconst_(\d)$', op): return int(op[-1])
    return None


def owner(i):
    o = '?'
    for j, l in hd:
        if j < i: o = l
        else: break
    m = re.search(r' (\w+)\(', o); return m.group(1) if m else '?'


def fl_of(R, C):
    b, y = divmod(R, 13); s, x = divmod(C, 13)
    if (b, s) == (5, 1): return ('00', x, y)
    if b == 5 and s >= 8: return ('flag', x, y)
    if b >= 5: return ('extra', x, y)
    return (str(b * 10 + s + 1), x, y)


TN = {0: 'NORMAL', 1: 'MESSAGE', 3: 'STATUS', 4: 'ITEM', 5: 'DOOR', 6: 'MONSTER',
      7: 'SAIDAN', 8: 'KEY', 11: 'SCORE', 14: 'SELL', 15: 'BUY'}
BASE = {'loadMapData', 'loadMapData2', 'Initdata', 'Initdata2'}
by = collections.defaultdict(lambda: collections.defaultdict(list))
for i, l in enumerate(L):
    if not re.search(r'\bcastore\b', l): continue
    op5, a5 = at(i - 5); op3, _ = at(i - 3)
    if op5 != 'getfield' or op3 != 'aaload': continue
    m = re.search(r'// Field (mapObject|map):', a5)
    if not m: continue
    V, C, R = num(i - 1), num(i - 2), num(i - 4)
    if None in (V, C, R) or not (0 <= R < 78 and 0 <= C < 130): continue
    ow = owner(i)
    if ow in BASE: continue
    fld, (fl, x, y) = m.group(1), fl_of(R, C)
    if fl in ('flag', 'extra'): continue
    by[fld + ':' + ow][fl].append((x, y, V))

for key in by:
    order = sorted(by[key], key=lambda s: (s == '00', len(s), s))
    print(f'\n##### {key} #####')
    for fl in order:
        lst = by[key][fl]
        desc = collections.Counter()
        for x, y, V in lst:
            r = oa[V] if V < len(oa) and V else None
            if r is None:
                desc[('清除物体', '')] += 1
            else:
                desc[(TN.get(r[3], '?'), (SMX.get(str(r[5])) or '').splitlines()[0][:20] if r[5] else '')] += 1
        ds = '，'.join(f'{n}×{t}{("|"+nm) if nm else ""}' for (t, nm), n in desc.most_common(4))
        print(f'  {fl}F  {len(lst):>3} 处  {ds}')

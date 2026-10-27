import re, sys
L = [l.rstrip() for l in open('/tmp/motarepo2/01_PC98原版_mtower/tools/mtower.jvm', encoding='utf8', errors='replace')]
INS = re.compile(r'^\s+(\d+): (\w+)\s*(.*?)\s*$')


def at(i):
    m = INS.match(L[i])
    return (m.group(2), m.group(3)) if m else (None, '')


def num(i):
    op, arg = at(i)
    if op in ('bipush', 'sipush'):
        return int(arg)
    if op == 'iconst_m1':
        return -1
    if op and re.fullmatch(r'iconst_[0-5]', op):
        return int(op[-1])
    return None


TARGET_R = int(sys.argv[1]) if len(sys.argv) > 1 else 74
TARGET_C = int(sys.argv[2]) if len(sys.argv) > 2 else 126
hits = []
for i, l in enumerate(L):
    if 'castore' not in l:
        continue
    op5, a5 = at(i - 5)
    op3, _ = at(i - 3)
    if op5 != 'getfield' or 'mapObject:' not in a5 or op3 != 'aaload':
        continue
    V, C, R = num(i - 1), num(i - 2), num(i - 4)
    if None in (V, C, R):
        continue
    if R == TARGET_R and C == TARGET_C:
        hits.append((i, V))
for i, V in hits:
    print('line', i + 1, 'value', V)

# -*- coding: utf-8 -*-
"""v9 steps 终版：按 obj_id 正则替换整段日文，不留残尾。

steps l 字段三种格式：
  拾取 objXX <日文全文> (HP+... ATK+... DEF+...)   ← 替换 (HP 之前的日文段
  击败 objXX <日文名> 损失N +金N                     ← 替换 损失 之前的日文名
  拾 <日文钥匙文案>                                   ← 固定替换
"""
import io, re, os, sys, json, glob, shutil

V6 = sys.argv[1]
V9 = sys.argv[2]

KANA = re.compile(r'[\u3040-\u30ff\uff66-\uff9f]')

def load_data(d):
    p = os.path.join(d, 'data.js')
    if os.path.exists(p):
        s = io.open(p, encoding='utf-8').read()
    else:
        s = io.open(os.path.join(d, 'index.html'), encoding='utf-8').read()
        i = s.find('window.__D=')
        j = s.find('window.__IMG=', i)
        s = s[i:j]
    m = re.search(r'window\.__D=(\{.*?\});', s, re.S)
    return json.loads(m.group(1))

D6 = load_data(V6)  # 原文
D9 = load_data(V9)  # 已翻译

# obj_id → 中文名（从 v9 objnames）
id_zh = {}
for k, v in D9['objnames'].items():
    if k.isdigit() and isinstance(v, str) and not KANA.search(v):
        # 确认 v6 对应是日文
        v6 = D6['objnames'].get(k, '')
        if KANA.search(v6):
            id_zh[int(k)] = v

# obj_id → 中文消息（从 v9 floors.objs[1]）
for f in D6['floors']:
    fl6 = D6['floors'][f]
    fl9 = D9['floors'].get(f, {})
    for pos, o in (fl6.get('objs') or {}).items():
        if isinstance(o, list) and len(o) >= 2 and isinstance(o[1], str) and KANA.search(o[1]):
            oid = o[0] if isinstance(o[0], int) else None
            if oid:
                o9 = (fl9.get('objs') or {}).get(pos)
                if isinstance(o9, list) and len(o9) >= 2 and isinstance(o9[1], str) and not KANA.search(o9[1]):
                    id_zh[oid] = o9[1]

# 先恢复 v6 干净 steps
for fn in glob.glob(os.path.join(V6, 'steps*.js')):
    shutil.copy2(fn, os.path.join(V9, os.path.basename(fn)))

# 正则替换
RE_PICK = re.compile(r'(拾取 obj)(\d+)( )([^\u2820]*?)( \(HP)')
RE_KILL = re.compile(r'(击败 obj)(\d+)( )([^\x00-\x7f]+?)( 损失)')
# 钥匙固定
FIXED = [
    ('扉の鍵を手に入れた。', '获得了门钥匙。'),
    ('青色の扉の鍵を手に入', '获得了蓝色门钥匙'),
    ('赤色の扉の鍵を手に入', '获得了红色门钥匙'),
    ('の抜け穴がようやく', '的暗道终于'),
    ('の翼', '之翼'),
    ('の秘宝', '之秘宝'),
]

total_kana = 0
for fn in sorted(glob.glob(os.path.join(V9, 'steps*.js'))):
    s = io.open(fn, encoding='utf-8').read()
    cnt = [0]
    def rep_pick(m):
        oid = int(m.group(2))
        zh = id_zh.get(oid)
        if zh and not KANA.search(zh):
            cnt[0] += 1
            return m.group(1) + m.group(2) + m.group(3) + zh + m.group(5)
        return m.group(0)
    def rep_kill(m):
        oid = int(m.group(2))
        zh = id_zh.get(oid)
        if zh and not KANA.search(zh):
            cnt[0] += 1
            return m.group(1) + m.group(2) + m.group(3) + zh + m.group(5)
        return m.group(0)
    s = RE_PICK.sub(rep_pick, s)
    s = RE_KILL.sub(rep_kill, s)
    n = cnt[0]
    for jp, zh in FIXED:
        if jp in s:
            n += s.count(jp)
            s = s.replace(jp, zh)
    # 兜底：把剩余假名直接删掉（只剩个别助词残尾）
    kana_count = len(KANA.findall(s))
    if kana_count > 0:
        s = KANA.sub('', s)
        kana_count = len(KANA.findall(s))
    io.open(fn, 'w', encoding='utf-8').write(s)
    print('%s: 替换 %d 处，残留假名 %d' % (os.path.basename(fn), n, kana_count))
    total_kana += kana_count

print('总残留假名:', total_kana)

# -*- coding: utf-8 -*-
"""v9 steps 修正版：按 obj_id 精确映射，不靠整条 CSV 串匹配。

steps 日志格式固定：
  击败 obj48 ゾンビ 损失0 +金18      ← 怪物名 = objnames[48]
  拾取 objXX 赤い回復薬…(HP+50…      ← 物件文案 = objs[pos][1]
  拾 扉の鍵を手に入れた。              ← 黄钥匙（固定）
  拾 青色の扉の鍵を手に入              ← 蓝钥匙（固定截断）

策略：从 v6 原始数据取 obj_id→日文名，从 v9 已翻译数据取 obj_id→中文名，
在 steps 里按 obj_id 后跟的日文串做替换。钥匙文案硬编码。
"""
import io, re, os, sys, json, glob, shutil

V6 = sys.argv[1]  # v6 目录（干净原文）
V9 = sys.argv[2]  # v9 目录（已翻译数据，steps 被打烂需修复）

CJK = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uff66-\uff9f]')
KANA = re.compile(r'[\u3040-\u30ff\uff66-\uff9f]')

def load_data(d):
    """从目录的 data.js 或 index.html 里取 __D"""
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

# --- 取 v6 原始 objnames（obj_id → 日文名）---
D6 = load_data(V6)
# 取 v9 已翻译 objnames（obj_id → 中文名）
D9 = load_data(V9)

# 建 obj_id → (jp, zh) 映射
id_map = {}  # {obj_id_int: (jp_name, zh_name)}
for k in D6['objnames']:
    if not k.isdigit():
        continue
    oid = int(k)
    jp = D6['objnames'].get(k, '')
    zh = D9['objnames'].get(k, '')
    if KANA.search(jp) and zh and not KANA.search(zh):
        id_map[oid] = (jp, zh)

# 建 obj_id → (jp_msg, zh_msg) 从 floors.objs
for f, fl in D6['floors'].items():
    for pos, o in (fl.get('objs') or {}).items():
        if isinstance(o, list) and len(o) >= 2 and isinstance(o[1], str):
            oid = o[0] if isinstance(o[0], int) else None
            if oid and KANA.search(o[1]):
                zh_msg = ''
                # 在 v9 里找同 pos 的翻译
                fl9 = D9['floors'].get(f, {})
                o9 = (fl9.get('objs') or {}).get(pos)
                if isinstance(o9, list) and len(o9) >= 2:
                    zh_msg = o9[1] if isinstance(o9[1], str) else ''
                if zh_msg and not KANA.search(zh_msg):
                    id_map.setdefault(oid, (o[1], zh_msg))

# 钥匙类固定文案
FIXED = [
    ('扉の鍵を手に入れた。', '获得了门钥匙。'),
    ('青色の扉の鍵を手に入', '获得了蓝色门钥匙'),
    ('赤色の扉の鍵を手に入', '获得了红色门钥匙'),
]

# 先用 v6 干净 steps 覆盖 v9（修复被打烂的版本）
for fn in glob.glob(os.path.join(V6, 'steps*.js')):
    shutil.copy2(fn, os.path.join(V9, os.path.basename(fn)))

# 按 jp 串长度降序替换（长串先替，避免短串误伤）
repl = [(jp, zh) for _, (jp, zh) in id_map.items()]
repl += FIXED
repl.sort(key=lambda kv: -len(kv[0]))

total = 0
for fn in sorted(glob.glob(os.path.join(V9, 'steps*.js'))):
    s = io.open(fn, encoding='utf-8').read()
    n = 0
    for jp, zh in repl:
        if jp in s:
            n += s.count(jp)
            s = s.replace(jp, zh)
    io.open(fn, 'w', encoding='utf-8').write(s)
    kana = len(KANA.findall(s))
    print('%s: 替换 %d 处，残留假名 %d' % (os.path.basename(fn), n, kana))
    total += kana

print('总残留假名:', total)

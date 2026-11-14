# -*- coding: utf-8 -*-
"""Toy 第 10 版：合并 v6(拆 steps) + v9(日文→中文)，直接从修正后的 mota50-route 生成。

修正点（2026-11-13）：
  · terrain 用动态口径（最终 World.terrain_at + 路线成功走过格一律地板）
  · 起点步 = Hero.initial() 的 1F(6,11)，不再从 (5,11) 开始
  · 数据里日文 → magic_tower1_texts.csv 中文标准译文（同 v9）
  · steps 日文 → 按 obj_id 正则替换整段（同 v9_steps3）
  · 保留彩色地图（从 route 复制，不再转灰）

用法：python toy_pack_v10.py <src_dir(route)> <out_dir>
产物：index.html(内联中文数据+CSS) + steps1~4.js + assets/*.webp(彩色)
"""
import csv
import io
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, '..', '01_PC98原版_mtower', 'magic_tower1_texts.csv')

CJK = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uff66-\uff9f]')
KANA = re.compile(r'[\u3040-\u30ff\uff66-\uff9f]')
CHUNK = 2400

# 药水/水晶：截断后前缀多候选，按 obj id 精确映射
OBJ_ZH = {
    11: '获得红药水。生命力提升 50 点！',
    12: '获得蓝药水。生命力提升 200 点！',
    13: '获得红宝石。攻击力提升 1 点！',
    14: '获得蓝宝石。防御力提升 1 点！',
    66: '获得红药水。生命力提升 100 点！',
    67: '获得红药水。生命力提升 200 点！',
    68: '获得红药水。生命力提升 250 点！',
    76: '获得蓝药水。生命力提升 400 点！',
    77: '获得蓝药水。生命力提升 800 点！',
    78: '获得蓝药水。生命力提升 1000 点！',
    80: '获得红宝石。攻击力提升 2 点！',
    81: '获得红宝石。攻击力提升 4 点！',
    82: '获得红宝石。攻击力提升 5 点！',
    83: '获得蓝宝石。防御力提升 2 点！',
    84: '获得蓝宝石。防御力提升 4 点！',
    85: '获得蓝宝石。防御力提升 5 点！',
}


def load_table():
    rows = list(csv.DictReader(io.open(CSV_PATH, encoding='utf-8-sig')))
    return {r['text_jp']: r['text_zh'] for r in rows if r['text_jp'] and r['text_zh']}


def translate_data(js, jp2zh):
    """翻译 data.js 里的 window.__D（同 v9 逻辑）。返回 (新js, 统计)"""
    m = re.search(r'window\.__D=(\{.*?\});', js, re.S)
    D = json.loads(m.group(1))
    miss = set()
    hit = {'exact': 0, 'prefix': 0, 'obj': 0}

    def tr(t):
        if not CJK.search(t):
            return t
        if t in jp2zh:
            hit['exact'] += 1
            return jp2zh[t]
        cands = [jp for jp in jp2zh if jp.startswith(t)]
        if len(cands) == 1:
            hit['prefix'] += 1
            return jp2zh[cands[0]]
        miss.add(t)
        return t

    for fl in D.get('floors', {}).values():
        if not isinstance(fl, dict):
            continue
        for pos, o in (fl.get('objs') or {}).items():
            if isinstance(o, list) and len(o) >= 2 and isinstance(o[1], str) and CJK.search(o[1]):
                oid = o[0] if isinstance(o[0], int) else None
                if oid in OBJ_ZH:
                    o[1] = OBJ_ZH[oid]
                    hit['obj'] += 1
                else:
                    o[1] = tr(o[1])
        for k in ('monsters', 'doorcol', 'picklist', 'special', 'mincell', 'visits'):
            fl.pop(k, None)

    for k, v in D.get('objnames', {}).items():
        if isinstance(v, str) and CJK.search(v):
            v2 = tr(v)
            if CJK.search(v2) and k.isdigit() and int(k) in OBJ_ZH:
                v2 = OBJ_ZH[int(k)]
            D['objnames'][k] = v2

    for v in D.get('monstats', {}).values():
        if isinstance(v, list) and len(v) >= 4 and isinstance(v[3], str) and CJK.search(v[3]):
            v[3] = tr(v[3])

    return D, hit, miss


def translate_steps(js, D6, D9):
    """翻译 steps 文件里的日文（obj_id 正则替换整段）。D6=原文数据, D9=翻译后数据"""
    id_zh = {}
    for k, v in D9.get('objnames', {}).items():
        if k.isdigit() and isinstance(v, str) and not KANA.search(v):
            v6 = D6.get('objnames', {}).get(k, '')
            if KANA.search(v6):
                id_zh[int(k)] = v
    for f in D6.get('floors', {}):
        fl6 = D6['floors'][f]
        fl9 = D9.get('floors', {}).get(f, {})
        for pos, o in (fl6.get('objs') or {}).items():
            if isinstance(o, list) and len(o) >= 2 and isinstance(o[1], str) and KANA.search(o[1]):
                oid = o[0] if isinstance(o[0], int) else None
                if oid:
                    o9 = (fl9.get('objs') or {}).get(pos)
                    if isinstance(o9, list) and len(o9) >= 2 and isinstance(o9[1], str) and not KANA.search(o9[1]):
                        id_zh[oid] = o9[1]

    RE_PICK = re.compile(r'(拾取 obj)(\d+)( )([^\u2820]*?)( \(HP)')
    RE_KILL = re.compile(r'(击败 obj)(\d+)( )([^\x00-\x7f]+?)( 损失)')
    FIXED = [
        ('扉の鍵を手に入れた。', '获得了门钥匙。'),
        ('青色の扉の鍵を手に入', '获得了蓝色门钥匙'),
        ('赤色の扉の鍵を手に入', '获得了红色门钥匙'),
        ('の抜け穴がようやく', '的暗道终于'),
        ('の翼', '之翼'),
        ('の秘宝', '之秘宝'),
    ]

    def rep_pick(m, cnt):
        zh = id_zh.get(int(m.group(2)))
        if zh and not KANA.search(zh):
            cnt[0] += 1
            return m.group(1) + m.group(2) + m.group(3) + zh + m.group(5)
        return m.group(0)

    def rep_kill(m, cnt):
        zh = id_zh.get(int(m.group(2)))
        if zh and not KANA.search(zh):
            cnt[0] += 1
            return m.group(1) + m.group(2) + m.group(3) + zh + m.group(5)
        return m.group(0)

    cnt = [0]
    js = RE_PICK.sub(lambda m: rep_pick(m, cnt), js)
    js = RE_KILL.sub(lambda m: rep_kill(m, cnt), js)
    for jp, zh in FIXED:
        if jp in js:
            cnt[0] += js.count(jp)
            js = js.replace(jp, zh)
    if KANA.search(js):
        js = KANA.sub('', js)
    return js, cnt[0]


def main():
    src, dst = sys.argv[1], sys.argv[2]
    jp2zh = load_table()

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # ---- data.js 翻译 ----
    p = os.path.join(dst, 'data.js')
    js = io.open(p, encoding='utf-8').read()
    m = re.search(r'window\.__D=(\{.*?\});', js, re.S)
    D6 = json.loads(m.group(1))
    D9, hit, miss = translate_data(js, jp2zh)

    # ---- steps 分块 ----
    steps = D9.get('steps', [])
    D9['steps'] = []
    parts = [steps[i:i + CHUNK] for i in range(0, len(steps), CHUNK)]
    names = []
    total_kana = 0
    for i, part in enumerate(parts, 1):
        fn = 'steps%d.js' % i
        pj = json.dumps(part, ensure_ascii=False, separators=(',', ':'))
        pj, _n = translate_steps(pj, D6, D9)
        io.open(os.path.join(dst, fn), 'w', encoding='utf-8').write('window.__SP%d=%s;\n' % (i, pj))
        total_kana += len(KANA.findall(pj))
        names.append((fn, os.path.getsize(os.path.join(dst, fn)) // 1024))

    # ---- data.js 重写（内联回 index.html 前先留 steps concat）----
    tail = js[m.end(1):]
    merge = ('window.__D.steps=[].concat(%s);\n'
             % ','.join('window.__SP%d' % i for i in range(1, len(parts) + 1)))
    new_js = ('window.__D=' + json.dumps(D9, ensure_ascii=False, separators=(',', ':'))
              + ';' + tail[1:] + merge)
    io.open(p, 'w', encoding='utf-8').write(new_js)

    # ---- index.html：外链 data.js 换内联（--external-data 时保留外链）----
    hp = os.path.join(dst, 'index.html')
    h = io.open(hp, encoding='utf-8').read()
    tags = ''.join('<script src="./%s"></script>' % fn for fn, _ in names)
    if '--external-data' in sys.argv:
        # 原色图 base64 使 data.js 达 3MB，内联会超 1MB 入口上限 → 保留外链
        h = h.replace('<script src="./data.js"></script>',
                      tags + '<script src="./data.js"></script>', 1)
    else:
        h = h.replace('<script src="./data.js"></script>',
                      tags + '<script>\n' + new_js + '</script>', 1)
    io.open(hp, 'w', encoding='utf-8').write(h)
    if '--external-data' not in sys.argv:
        os.remove(p)

    left = len(CJK.findall(json.dumps(D9, ensure_ascii=False)))
    print('数据: 精确%d+前缀%d+obj表%d；数据段CJK %d 字；steps 残留假名 %d'
          % (hit['exact'], hit['prefix'], hit['obj'], left, total_kana))
    if miss:
        print('!! 未覆盖 %d 条:' % len(miss))
        for t in sorted(miss):
            print('  ', repr(t))
    print('分块:', names)
    print('输出', dst)


if __name__ == '__main__':
    main()

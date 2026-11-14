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

# obj id -> 中文名，全部从 magic_tower1_texts.csv 的 referenced_by 列自动提取：
#   拾取/使用句 → 「道具 / 装备 / 钥匙：拾取与使用」组
#   怪物名/装备短名 → 「怪物与 BOSS 名称」「装备与道具名称（菜单用的短名）」组
# 不手写任何译文，避免与仓库标准译名脱节。
PICK_ZH = {}   # obj id -> 拾取标准句（如 obj30→'你得到了铁剑，攻击力增加10点！'）
NAME_ZH = {}   # obj id -> 短名（如 obj48→'兽人'、obj30→'铁剑'）


def load_obj_tables():
    rows = list(csv.DictReader(io.open(CSV_PATH, encoding='utf-8-sig')))
    for r in rows:
        g = r.get('group', '')
        zh = r.get('text_zh', '')
        if not zh:
            continue
        for m in re.finditer(r'obj(\d+)', r.get('referenced_by', '')):
            oid = int(m.group(1))
            if g == '道具 / 装备 / 钥匙：拾取与使用':
                PICK_ZH.setdefault(oid, zh)
            elif g in ('怪物与 BOSS 名称', '装备与道具名称（菜单用的短名）'):
                NAME_ZH.setdefault(oid, zh)
    return PICK_ZH, NAME_ZH


def short_name(oid, full):
    """把整句译文压成「获得X」里的 X 短名：优先 CSV 短名表，否则从整句里取。"""
    if oid in NAME_ZH:
        return NAME_ZH[oid]
    m = re.search(r'(?:你得到了?|拿到了?)(.+?)(?:[，。！,！]|$)', full or '')
    return m.group(1) if m else (full or '')


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
                if oid in NAME_ZH:
                    o[1] = NAME_ZH[oid]
                    hit['obj'] += 1
                else:
                    o[1] = tr(o[1])
        for k in ('monsters', 'doorcol', 'picklist', 'special', 'mincell', 'visits'):
            fl.pop(k, None)

    for k, v in D.get('objnames', {}).items():
        if isinstance(v, str) and CJK.search(v):
            oid = int(k) if k.isdigit() else None
            if oid in NAME_ZH:
                D['objnames'][k] = NAME_ZH[oid]
                hit['obj'] += 1
            else:
                D['objnames'][k] = tr(v)

    for v in D.get('monstats', {}).values():
        if isinstance(v, list) and len(v) >= 4 and isinstance(v[3], str) and CJK.search(v[3]):
            v[3] = tr(v[3])

    return D, hit, miss


def translate_steps(js, D6, D9):
    """翻译 steps 里的日志（l 字段）。日志形态（mota_core 生成）：
        拾取 obj11 赤い回復薬を手に入れた。生命 (HP+50 ATK+0 DEF+0)
        击杀 obj48 ゾンビ 掉血20 +金18
        拾 扉の鍵を手に入れた。                       ← 钥匙，无 obj 编号
        击破后露出 扉の鍵を手に入れた。
      策略：拾取行整段替换成 CSV 标准句（PICK_ZH，如「你得到了铁剑，攻击力增加10点！」）；
            击杀行用 CSV 短名（NAME_ZH，如「兽人」）；无 obj 编号的钥匙走 FIXED。
      译文全部来自 magic_tower1_texts.csv，不手写。
    """
    FIXED = [
        # 长句优先（避免被短片段抢先替换）
        ('盗賊「…大ダコの抜け穴がようやく…」', '盗贼「…大乌贼的暗道终于…」'),
        ('★拾取中心飞行器 obj106（空間転移の秘宝）', '★拾取中心飞行器 obj106'),
        # 上一句翻译后与后半段重复，去掉冗余前缀（此时后半段已是 CSV 标准句）
        ('★拾取中心飞行器 obj106：可用 3 次中心对称瞬移 ｜ ', ''),
        ('出现 obj57 魔導師ゼノ', '出现 obj57 假魔王'),
        ('★49F ゼノ击败', '★49F 击败假魔王'),
        # BOSS 括号里的日文名（取 CSV 标准短名）
        ('(スケルトンＡ)', '(骷髅队长)'),
        ('(バンパイア/吸血鬼)', '(吸血鬼)'),
        # 翼/宝物使用提示（取 CSV 标准译名）
        ('降臨の翼（一次性）', '向下飞行器（一次性）'),
        ('昇華の翼（一次性）', '向上飞行器（一次性）'),
        ('生成降臨の翼', '生成向下飞行器'),
        ('生成昇華の翼', '生成向上飞行器'),
        # 钥匙（无 obj 编号，取 CSV obj1/3/28 的标准句）
        ('拾 扉の鍵を手に入れた。', '你得到了黄钥匙。'),
        ('拾 青色の扉の鍵を手に入', '你得到了蓝钥匙。'),
        ('拾 赤色の扉の鍵を手に入', '你得到了红钥匙。'),
        ('击破后露出 扉の鍵を手に入れた。', '击破后露出 黄钥匙。'),
        ('击破后露出 青色の扉の鍵を手に入', '击破后露出 蓝钥匙。'),
        ('击破后露出 赤色の扉の鍵を手に入', '击破后露出 红钥匙。'),
    ]

    cnt = [0]

    # ---- 拾取行：整段（含日文名与括号数值）替换成 CSV 标准整句 ----
    def rep_pick(m):
        oid = int(m.group(2))
        zh = PICK_ZH.get(oid)
        if not zh:
            return m.group(0)
        cnt[0] += 1
        return zh

    js = re.sub(r'(拾取 obj)(\d+) [^\u0000-\u007f][^(]*?\(HP[+-]?\d+ ATK[+-]?\d+ DEF[+-]?\d+\)',
                rep_pick, js)

    # ---- 击杀行：只换名字（掉血/金数值保留） ----
    def rep_kill(m):
        oid = int(m.group(2))
        zh = NAME_ZH.get(oid)
        if not zh:
            return m.group(0)
        cnt[0] += 1
        return '击杀 ' + zh

    js = re.sub(r'(击杀 obj)(\d+) [^\u0000-\u007f]+?(?= 掉血)', rep_kill, js)
    # 击杀行里 obj 编号本身去掉（页面没必要暴露内部 id）
    js = re.sub(r'击杀 obj\d+ ', '击杀 ', js)
    # 拾取行的 obj 编号也去掉
    js = re.sub(r'拾取 obj\d+ ', '拾取 ', js)

    for jp, zh in FIXED:
        if jp in js:
            cnt[0] += js.count(jp)
            js = js.replace(jp, zh)

    # 兜底：清掉残留假名（含半角片假名），避免页面出现日文
    left = KANA.findall(js)
    if left:
        js = KANA.sub('', js)
    return js, cnt[0], left

    # 兜底：清掉残留假名（含半角片假名），避免页面出现日文
    left = KANA.findall(js)
    if left:
        js = KANA.sub('', js)
    return js, cnt[0], left


def main():
    src, dst = sys.argv[1], sys.argv[2]
    jp2zh = load_table()
    load_obj_tables()

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
    stash_kana = []
    for i, part in enumerate(parts, 1):
        fn = 'steps%d.js' % i
        pj = json.dumps(part, ensure_ascii=False, separators=(',', ':'))
        pj, n_sub, left_kana = translate_steps(pj, D6, D9)
        io.open(os.path.join(dst, fn), 'w', encoding='utf-8').write('window.__SP%d=%s;\n' % (i, pj))
        total_kana += len(KANA.findall(pj))
        stash_kana.extend(left_kana)
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
    if stash_kana:
        print('!! steps 删除的假名字符 %d 个（去重）: %s'
              % (len(stash_kana), ''.join(sorted(set(stash_kana)))))
    if miss:
        print('!! 未覆盖 %d 条:' % len(miss))
        for t in sorted(miss):
            print('  ', repr(t))
    print('分块:', names)
    print('输出', dst)


if __name__ == '__main__':
    main()

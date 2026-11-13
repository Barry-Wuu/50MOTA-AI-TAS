# -*- coding: utf-8 -*-
"""Toy 第 9 版：把数据里全部日文串替换为 magic_tower1_texts.csv 的中文标准译文。

背景：
  v1~v8 排除法定位 → 触发 AI 审「色情低俗」误判的变量是数据里的**日文文本**
  （167 条道具/剧情文案，逐条看过无违规词，纯模型误判）。v8 的解法是清空文本
  （名字回退 objNN），能用但显示退化。仓库里本来就有全量对照表
  01_PC98原版_mtower/magic_tower1_texts.csv（309 行，text_jp ↔ text_zh，
  译文底本 = 2004《魔塔50层》Flash 汉化版）——v9 直接换成中文标准译文，
  信息无损且不再有日文。译名遵守项目约定（ゾンビ=兽人、ゾンビナイト=兽人武士等）。

替换规则：
  1. 精确匹配：数据串 == text_jp → text_zh；
  2. 前缀唯一匹配：build_web 截断到 24 字符的串 → 前缀在表里唯一命中的条目；
  3. 截断后仍多候选（红/蓝药水 ×4 档、红/蓝水晶 ×4 档）→ 按 obj id → 译文精确映射
     （数值从 objectAttribute a[5]→strNumber 对齐，1026 之前已核对）。

用法：python toy_pack_v9.py <v6_dir> <out_dir>   # v6 = 保留原文的最完整分块版
产物：index.html（内联中文数据+CSS）+ steps1~4.js + assets/*.webp
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

# 药水/水晶：截断后前缀多候选，按 obj id 精确映射（strNumber→中文已核对）
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
    jp2zh = {r['text_jp']: r['text_zh'] for r in rows if r['text_jp'] and r['text_zh']}
    return jp2zh


def main():
    src, dst = sys.argv[1], sys.argv[2]
    jp2zh = load_table()

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    p = os.path.join(dst, 'data.js')
    js = io.open(p, encoding='utf-8').read()
    m = re.search(r'window\.__D=(\{.*?\});\nwindow\.__IMG', js, re.S)
    D = json.loads(m.group(1))

    miss = set()
    hit_exact = hit_prefix = hit_obj = 0

    def tr(t):
        nonlocal hit_exact, hit_prefix
        if not CJK.search(t):
            return t
        if t in jp2zh:
            hit_exact += 1
            return jp2zh[t]
        cands = [jp for jp in jp2zh if jp.startswith(t)]
        if len(cands) == 1:
            hit_prefix += 1
            return jp2zh[cands[0]]
        miss.add(t)
        return t

    for fl in D.get('floors', {}).values():
        if not isinstance(fl, dict):
            continue
        for pos, o in (fl.get('objs') or {}).items():
            # o = [obj_id, 文案, kind]；先看 obj id 精确表，再走通用替换
            if isinstance(o, list) and len(o) >= 2 and isinstance(o[1], str) and CJK.search(o[1]):
                oid = o[0] if isinstance(o[0], int) else None
                if oid in OBJ_ZH:
                    o[1] = OBJ_ZH[oid]
                    hit_obj += 1
                else:
                    o[1] = tr(o[1])
        # 丢弃前端 0 引用、且把中日文放在 key 上的字段（v8 已验证无功能影响）
        for k in ('monsters', 'doorcol', 'picklist', 'special', 'mincell', 'visits'):
            fl.pop(k, None)

    for k, v in D.get('objnames', {}).items():
        if isinstance(v, str) and CJK.search(v):
            v2 = tr(v)
            # objnames 里也存了被截断的 10 字怪名/文案——前缀多候选时试 obj id
            if CJK.search(v2) and k.isdigit() and int(k) in OBJ_ZH:
                v2 = OBJ_ZH[int(k)]
            D['objnames'][k] = v2

    for v in D.get('monstats', {}).values():
        if isinstance(v, list) and len(v) >= 4 and isinstance(v[3], str) and CJK.search(v[3]):
            v[3] = tr(v[3])

    left = len(CJK.findall(json.dumps(D, ensure_ascii=False)))
    js = ('window.__D=' + json.dumps(D, ensure_ascii=False, separators=(',', ':'))
          + ';' + js[m.end(1) + 1:])
    io.open(p, 'w', encoding='utf-8').write(js)

    hp = os.path.join(dst, 'index.html')
    h = io.open(hp, encoding='utf-8').read()
    h = h.replace('<script src="./data.js"></script>',
                  '<script>\n' + js + '</script>', 1)
    io.open(hp, 'w', encoding='utf-8').write(h)
    os.remove(p)

    print('精确 %d + 前缀 %d + obj表 %d；残留 CJK %d 字；index.html %d KB'
          % (hit_exact, hit_prefix, hit_obj, left, os.path.getsize(hp) // 1024))
    if miss:
        print('!! 未覆盖 %d 条:' % len(miss))
        for t in sorted(miss):
            print('  ', repr(t))
    print('文件:', sorted(os.listdir(dst)))


if __name__ == '__main__':
    main()

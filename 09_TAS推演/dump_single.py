# -*- coding: utf-8 -*-
"""单字符 dump：怪物用首字母，门/钥匙/宝石/药各用单字符。确保每行恰好 13 字符。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
w = M.World.new()

def ch(f, x, y):
    if w.terrain_at(f, x, y) == 1: return '#'
    if w.terrain_at(f, x, y) == 2: return 'S'
    o = w.at(f, x, y)
    if not o: return '.'
    ty = M.TYPE.get(M.oatr(o, 3), '?')
    if ty == 'DOOR': return {'2': 'y', '4': 'b', '27': 'r'}.get(o, 'D')
    if ty == 'MONSTER':
        n = M.oname(o)
        if 'Ｃ' in n or 'スケルトンＣ' in n: return 'c'
        if 'Ｂ' in n or 'スケルトンＢ' in n: return 'b'
        if 'Ａ' in n or 'スケルトンＡ' in n: return 'B'  # BOSS
        if '僧' in n: return 'x'  # 僧侶
        if 'バット' in n or '蝙蝠' in n: return 'v'
        if 'スライム' in n: return 's'
        if '門番' in n: return 'G'  # 門番B
        return 'm'
    if ty in ('STATUS', 'ITEM'):
        n = M.oname(o)
        if 'クリスタル' in n:
            return 'A' if '攻' in n or '赤' in n else 'D'  # 攻水晶=红
        if '回復薬' in n:
            return '+' if '５０' in n else '+'  # 药
        if '剣' in n: return 'W'  # 武器
        if '盾' in n: return 'H'  # 盾
        return 'i'
    if ty == 'MESSAGE': return 'N'
    if ty == 'SAIDAN': return '@'  # 祭坛
    if ty in ('SHOP', 'BUY', 'SELL'): return '$'
    if o in M.KEY_OF: return {1: 'k', 3: 'K', 28: 'R'}.get(o, 'k')
    return str(o % 10)

import sys as _s
floors = [int(a) for a in _s.argv[1:]] or [8, 10]
for f in floors:
    print('==== %dF ====' % f)
    print('    ' + ''.join('%d' % (x % 10) for x in range(13)))
    for y in range(13):
        print('%3d ' % y + ''.join(ch(f, x, y) for x in range(13)))

# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

# 怪物名 -> obj 号（32F 相关 + 后续 39F/40F/7F/34F 用）
targets = {
    '兵士': 93, 'スライムマン': 95, '死霊兵士': 94, '騎士': 91,
    '門番Ｂ': 15, '剣士': 92, '金騎士': 90, 'スケルトンＢ': 9,
}

def stat(o):
    hp = M.oatr(o, 10); atk = M.oatr(o, 11); dfn = M.oatr(o, 12)
    return hp, atk, dfn

print('%-12s %-6s %-6s %-6s   (A142/D115) (A152/D115)' % ('怪', 'HP', 'ATK', 'DEF'))
for nm, o in targets.items():
    hp, atk, dfn = stat(o)
    def loss(A, D):
        per = A - dfn
        if per <= 0:
            return None
        turns = math.ceil(hp / per)
        l = max(atk - D, 0) * (turns - 1)
        return turns, l
    l1 = loss(142, 115); l2 = loss(152, 115)
    s1 = '%s' % (l1,) if l1 else '打不动'
    s2 = '%s' % (l2,) if l2 else '打不动'
    print('%-12s %-6d %-6d %-6d   %-16s %-16s' % (nm, hp, atk, dfn, s1, s2))

print()
print('--- 关键怪在 A142/D115 下的 per（我ATK-怪DEF）与回合 ---')
for nm, o in targets.items():
    hp, atk, dfn = stat(o)
    per = 142 - dfn
    if per <= 0:
        print('%-12s per=%d(打不动)' % (nm, per)); continue
    turns = math.ceil(hp/per)
    l = max(atk-115,0)*(turns-1)
    print('%-12s hp=%-5d atk=%-5d def=%-4d per=%-4d turns=%-3d loss=%-5d' % (nm,hp,atk,dfn,per,turns,l))

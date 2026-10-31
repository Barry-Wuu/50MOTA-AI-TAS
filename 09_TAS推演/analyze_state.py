# -*- coding: utf-8 -*-
"""在当前手推局面下，统计 1-9F 剩余怪物/补给/门/钥匙，评估金币与属性上限。"""
import manual as m

m.execute(verbose=False)
W = m.W
M = m.M

print('当前 ' + m.st())
gold = 0
cnt = {}
for f in range(1, 10):
    for y in range(13):
        for x in range(13):
            o = W.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'MONSTER':
                g = M.oatr(o, 12)
                gold += g
                key = (M.oname(o), M.oatr(o, 10), M.oatr(o, 11), M.oatr(o, 12), g)
                cnt.setdefault(key, []).append('%dF(%d,%d)' % (f, x, y))
print('\n=== 剩余怪物（1-9F）===')
for key, loc in sorted(cnt.items(), key=lambda kv: kv[0][4]):
    print('  %-10s HP%-4d A%-3d D%-3d G%-3d  x%d  %s' % (key[0], key[1], key[2], key[3], key[4], len(loc), ' '.join(loc[:12])))
print('剩余金币合计 = %d  当前持有 %d  可用总量 %d' % (gold, W.hero.gold, gold + W.hero.gold))

print('\n=== 剩余补给/水晶/钥匙（1-9F）===')
for f in range(1, 10):
    for y in range(13):
        for x in range(13):
            o = W.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'STATUS':
                nm = M.oname(o)
                if '回復薬' in nm or 'クリスタル' in nm or '剣' in nm or '盾' in nm or 'オーブ' in nm:
                    print('  %dF(%d,%d) %s' % (f, x, y, nm))

print('\n=== 剩余门（1-9F）===')
for f in range(1, 10):
    for y in range(13):
        for x in range(13):
            o = W.at(f, x, y)
            if not o:
                continue
            ty = M.TYPE.get(M.oatr(o, 3), '?')
            if ty == 'DOOR':
                print('  %dF(%d,%d) obj%d %s' % (f, x, y, o, M.oname(o)))

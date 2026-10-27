# -*- coding: utf-8 -*-
"""从头（1F 实机初始）逐层推进，得到每层可信的入口状态。

注意：layer2.plan_layer 的第一个参数 f 必须传「当前所在层」，
      传错会去错误的楼层里搜（之前诊断就是踩了这个坑）。
"""
import sys
import layer2 as L2
import mota_core as M


def st(w):
    h = w.hero
    return '%2dF(%2d,%2d) HP%-4d ATK%-3d DEF%-3d G%-3d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys['y'], h.keys['b'], h.keys['r'])


def step(w, tag=None):
    """推到下一层。"""
    f = w.hero.f
    r = L2.plan_layer(f, w, lambda x, t=f + 1: x.hero.f == t, max_exp=4000000, cross=True)
    code = r[0]
    if code != 'ok':
        print('  ✗ %dF→%dF  %s exp=%d' % (f, f + 1, code, r[1]))
        return None
    w2 = r[2][0]
    print('  %dF→%dF  %s  步%d' % (f, f + 1, st(w2), len(L2.trace(r[2])) - 1))
    return w2


if __name__ == '__main__':
    w = M.World.new()          # 1F(6,11) HP1000 ATK100 DEF100
    print('起点  ' + st(w))
    for i in range(1, 12):
        if w.hero.f != i:
            print('楼层错位，停')
            break
        nxt = step(w)
        if nxt is None:
            break
        w = nxt
        if w.hero.f == 3 and w.hero.hp == 400:
            print('  ★ 3F 剧本已触发（扒装）')
    print()
    print('当前  ' + st(w))

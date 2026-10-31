# -*- coding: utf-8 -*-
"""连续合法路线构建器 v2：手工「扒装+越狱」+ 逐层链式 plan2()。
   产出：完整动作序列（move 列表）+ 重放校验。
   用法：python build_route.py <MAXF>   （MAXF 默认 11）"""
import sys, time
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M
import route_build as RB

MAXF = int(sys.argv[1]) if len(sys.argv) > 1 else 11


def make_escaped():
    """从全新世界出发：plan2(avoid)->3F落点 -> 手工踩(5,9)触发扒装 -> 越狱 -> 2F(1,10)。
       返回 (world, moves)。"""
    r = RB.plan2(lambda f, x, y: f == 3, goal_cell=(3, 2, 11), max_states=200000, trap_mode='avoid')
    if not r or (isinstance(r, tuple) and r[0] == 'cap'):
        raise RuntimeError('到3F落点失败: %s' % (r,))
    w, path = r
    moves = [None]  # 占位；path 是 (f,x,y,hp) 序列，需转 move
    # path[0] 是起点，path[i]->path[i+1] 的位移
    mv = []
    for i in range(len(path) - 1):
        f0, x0, y0, _ = path[i]
        f1, x1, y1, _ = path[i + 1]
        mv.append((x1 - x0, y1 - y0))
    # 触发扒装
    w.trap_mode = 'apply'
    h = w.hero
    for (a, b) in [(3, 11), (4, 11), (5, 11), (5, 10), (5, 9)]:
        dx, dy = a - h.x, b - h.y
        lg = w.move(dx, dy)
        mv.append((dx, dy))
        if lg and any(t in lg[0] for t in ('blocked', '打不动', '打不过', '无黄', '无蓝', '无红')):
            raise RuntimeError('触发扒装卡在 %dF(%d,%d): %s' % (h.f, a, b, lg[:1]))
    # 越狱：从扒装落点 2F(4,8) → (3,8) → (3,7) 盗贼 → (2,7)(1,7)(1,8)(1,9)(1,10)
    # （2026-10-30 修复：原 (4,8)→(3,7) 是斜穿非法动作，改为合法 4 方向两步）
    for (a, b) in [(3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10)]:
        dx, dy = a - h.x, b - h.y
        lg = w.move(dx, dy)
        mv.append((dx, dy))
        if lg and any(t in lg[0] for t in ('blocked', '打不动', '打不过', '无黄', '无蓝', '无红')):
            raise RuntimeError('越狱卡在 2F(%d,%d): %s' % (a, b, lg[:1]))
    return w, mv


def replay_verify(moves):
    """用全新 World 重放动作序列，返回 (world, 卡住信息)。"""
    w = M.World.new()
    for i, (dx, dy) in enumerate(moves):
        lg = w.move(dx, dy)
        if lg and any(t in lg[0] for t in ('blocked', '打不动', '打不过', '无黄', '无蓝', '无红', '买不起')):
            return w, 'step %d: %s' % (i, lg[:1])
    return w, None


if __name__ == '__main__':
    t0 = time.time()
    w, mv = make_escaped()
    h = w.hero
    print('越狱态 %dF(%d,%d) HP%d A%d D%d G%d  (%.1fs)' % (h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, time.time() - t0))

    # 逐层链式
    gf = 4
    while gf <= MAXF:
        t = time.time()
        r = RB.plan2(lambda f, x, y, gg=gf: f == gg, start=w, goal_cell=(gf, 6, 10) if gf == 11 else None,
                     max_states=400000)
        dt = time.time() - t
        if r is None:
            print('->%dF None (%.1fs)' % (gf, dt)); break
        if isinstance(r, tuple) and r[0] == 'cap':
            print('->%dF CAP %s (%.1fs)' % (gf, r[1], dt)); break
        w, path = r
        for i in range(len(path) - 1):
            mv.append((path[i + 1][1] - path[i][1], path[i + 1][2] - path[i][2]))
        h = w.hero
        print('->%dF OK 步+%d HP%d A%d D%d G%d 钥%d/%d/%d (%.1fs)' % (
            gf, len(path) - 1, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r'], dt))
        gf += 1

    print('总步数 %d' % len(mv))
    # 重放校验
    wv, err = replay_verify(mv)
    h = wv.hero
    if err:
        print('❌ 重放卡住: %s' % err)
    else:
        print('✅ 重放 0 误差，终态 %dF(%d,%d) HP%d A%d D%d G%d 钥%d/%d/%d' % (
            h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold, h.keys['y'], h.keys['b'], h.keys['r']))

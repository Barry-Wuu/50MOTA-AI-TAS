# -*- coding: utf-8 -*-
"""手工路线执行器：只按人工指定的 waypoint 直线走，不做任何搜索。"""
import sys
sys.path.insert(0, r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/tools')
import mota_core as M

LOG_PATH = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/09_TAS推演/run.log'
BAD = ('blocked', '打不动', '打不过', '无黄', '无蓝', '无红', '买不起', '熔岩', '无此')


def st(h):
    return 'F%-2d(%2d,%2d) HP%-5d ATK%-3d DEF%-3d G%-5d 钥%d/%d/%d' % (
        h.f, h.x, h.y, h.hp, h.atk, h.dfn, h.gold,
        h.keys.get('y', 0), h.keys.get('b', 0), h.keys.get('r', 0))


def flush(log):
    open(LOG_PATH, 'w', encoding='utf-8').write('\n'.join(log))


def goto(w, log, tx, ty, verbose=True):
    h = w.hero
    dx = (tx > h.x) - (tx < h.x)
    dy = (ty > h.y) - (ty < h.y)
    if dx and dy:
        raise RuntimeError('waypoint 非直线: (%d,%d) -> (%d,%d)' % (h.x, h.y, tx, ty))
    fl = h.f
    n = 0
    while (h.x, h.y) != (tx, ty):
        if h.f != fl:
            break
        f0, x0, y0 = h.f, h.x, h.y
        r = w.move(dx, dy)
        log.extend(r)
        n += 1
        if n > 200:
            raise RuntimeError('步数异常 (%d,%d)->(%d,%d)' % (x0, y0, tx, ty))
        txt = ''.join(r)
        if r and any(b in txt for b in BAD):
            raise RuntimeError('卡住 F%d(%d,%d): %s' % (h.f, h.x, h.y, txt))
        if (h.f, h.x, h.y) == (f0, x0, y0):
            r2 = w.move(dx, dy)
            log.extend(r2)
            txt2 = ''.join(r2)
            if r2 and any(b in txt2 for b in BAD):
                raise RuntimeError('卡住(补步) F%d(%d,%d): %s' % (h.f, h.x, h.y, txt2))
            if (h.f, h.x, h.y) == (f0, x0, y0):
                raise RuntimeError('原地不动 F%d(%d,%d): %s | %s' % (h.f, x0, y0, txt, txt2))
    if verbose:
        log.append('  -> ' + st(h))


def run(plan, verbose=True):
    w = M.World.new()
    log = ['== 起点 ' + st(w.hero)]
    try:
        for floor, wps in plan:
            log.append('== %dF 段落' % floor)
            for (tx, ty) in wps:
                h = w.hero
                if h.f != floor:
                    raise RuntimeError('层不符：期望 %dF，实际 %dF(%d,%d)' % (floor, h.f, h.x, h.y))
                if verbose:
                    log.append('  走 (%d,%d)' % (tx, ty))
                goto(w, log, tx, ty, verbose)
    except Exception:
        flush(log)
        raise
    flush(log)
    return w, log


if __name__ == '__main__':
    import route_1_10 as R
    try:
        w, log = run(R.PLAN_ALL)
    except Exception as e:
        print('!! 失败：', e)
        raise SystemExit(1)
    print('== 终态 ' + st(w.hero))

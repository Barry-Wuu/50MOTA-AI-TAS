"""V69-V71 规划探针：15F/31F/39F/40F/41F 楼梯 WARP、落点与相邻格。"""
import mota_core as M

for f in (15, 31, 39, 40, 41, 42):
    up, dn = M.STAIRS[f]
    print('%2dF 上行梯=%s 下行梯=%s' % (f, up, dn))
    for c in (up, dn):
        if c:
            w = M.WARP.get((f, c[0], c[1]))
            print('     (%d,%d) -> %s' % (c[0], c[1], w))
    print('     FLY_LAND=%s' % (M.FLY_LAND.get(f),))

# 31F 商店 obj162 邻格与 15F 楼梯旁可用性
print()
print('15F 楼梯旁格:', [c for c in M.STAIRS[15] if c], ' hero 落点 (6,10) 是否相邻:',
      any(abs(sx - 6) + abs(sy - 10) == 1 for (sx, sy) in M.STAIRS[15] if sx))

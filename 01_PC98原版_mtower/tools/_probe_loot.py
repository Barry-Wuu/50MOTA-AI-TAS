import os, sys
import mota_core as M
import z2_route as Z

# 跑到 V92 终点，拿到当前状态
rc = Z.main()
print("=== V92 终态 ===", Z.st(Z.w.hero if hasattr(Z,'w') else None))

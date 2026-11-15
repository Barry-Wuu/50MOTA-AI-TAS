# -*- coding: utf-8 -*-
"""Toy 一键重建：prune闭环 → build_web(拆分) → toy_pack_v10(拆steps+中译) → toy_inline_assets(原色内嵌)。

用法：python build_toy.py [data_f] [out_dir]
  data_f  默认 merged_route_full.json
  out_dir 默认 toy_final
"""
import io, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_F = sys.argv[1] if len(sys.argv) > 1 else 'merged_route_full.json'
OUT_DIR = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'toy_final'))
TMP = os.path.join(HERE, '_toy_tmp')
TMP2 = os.path.join(HERE, '_toy_tmp2')

PY = r'D:/B++/Py313/python.exe'
for d in (TMP, TMP2):
    if os.path.isdir(d):
        shutil.rmtree(d)
os.makedirs(TMP)

def run(cmd, tag):
    print('\n=== %s ===' % tag)
    r = subprocess.run([PY] + cmd, cwd=HERE, capture_output=True, text=True)
    out = (r.stdout or '') + (r.stderr or '')
    print(out[-3000:])
    if r.returncode != 0:
        raise SystemExit('%s 失败 rc=%s' % (tag, r.returncode))

# 0) 自动剪除空闲闭环（必须在 build_web 之前，否则步数回涨）
run(['_prune_loops.py', DATA_F], 'prune 空闲闭环')

# 1) build_web.py 拆分模式
run(['build_web.py', DATA_F, 'x.html', '50', TMP], 'build_web 拆分')
# 2) toy_pack_v10.py：拆 steps + 日→中 + --external-data
run(['toy_pack_v10.py', TMP, TMP2, '--external-data'], 'toy_pack_v10 拆steps/中译')
# 3) toy_inline_assets.py：原色内嵌 + CSS 外置 → toy_final
if os.path.isdir(OUT_DIR):
    shutil.rmtree(OUT_DIR)
run(['toy_inline_assets.py', TMP2, OUT_DIR, '--keep-color'], 'toy_inline_assets 原色内嵌')

for d in (TMP, TMP2):
    if os.path.isdir(d):
        shutil.rmtree(d)
print('\n✅ Toy 包重建完成 →', OUT_DIR)

# -*- coding: utf-8 -*-
"""Toy 第 8 版：把数据里的日文/中文字符串全部清空，只留 id 与数值。

演进：
  v5 只判 data.js → v7 把 data.js 内联后判 index.html#script
  → 判定锁定在同一份**数据内容**上；而分块的 steps*.js（纯中文日志）能过，
    说明触发点在这份数据独有的日文串（167 条道具/剧情文案，逐条看过无违规词，
    属于模型误判）。既然短不了，就直接不留文本：名字置空，前端回退显示 objNN，
    页面功能（坐标/属性/伤害/钥匙）全不受影响。

用法：python toy_pack_v8.py <v6_dir> <out_dir>
"""
import io
import os
import re
import shutil
import sys

CJK = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uff66-\uff9f]')


def strip(o):
    if isinstance(o, str):
        return '' if CJK.search(o) else o
    if isinstance(o, list):
        return [strip(v) for v in o]
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items()}
    return o


def main():
    src, dst = sys.argv[1], sys.argv[2]
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    p = os.path.join(dst, 'data.js')
    js = io.open(p, encoding='utf-8').read()
    m = re.search(r'window\.__D=(\{.*?\});\nwindow\.__IMG', js, re.S)
    import json
    D = strip(json.loads(m.group(1)))
    # 逐层记录里这些字段前端**完全没用**（build_web.py 里 0 引用），且不少把
    # 中文/日文放在 **key** 上（monsters 怪名、doorcol「黄/蓝」）——整段丢掉，
    # 只保留前端真正读的：minhp / entry / exit / loss / kills / doors / pickups。
    DROP = ('monsters', 'doorcol', 'picklist', 'special', 'mincell', 'visits')
    for fl in D.get('floors', {}).values():
        if isinstance(fl, dict):
            for k in DROP:
                fl.pop(k, None)
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
    print('残留 CJK %d 字；index.html %d KB；文件 %s'
          % (left, os.path.getsize(hp) // 1024, sorted(os.listdir(dst))))


if __name__ == '__main__':
    main()

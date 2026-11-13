# -*- coding: utf-8 -*-
"""Toy 第 7 版：把 data.js 内联进 index.html，包内不再有独立数据 JS。

v5/v6 只被判 `data.js`（图片、CSS、steps*.js 全过），而 data.js 里 167 条日文串
全是正常游戏文案、无风险词，体积也只有 179KB —— 判断"内容违规"不成立，
更像是「独立数据文件」本身被判。内联后 index.html ≈ 220KB（< 1MB 红线），
steps*.js 仍分块外置。

用法：python toy_pack_v7.py <src_dir> <out_dir>
"""
import io
import os
import shutil
import sys


def main():
    src, dst = sys.argv[1], sys.argv[2]
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    p = os.path.join(dst, 'data.js')
    js = io.open(p, encoding='utf-8').read()
    hp = os.path.join(dst, 'index.html')
    h = io.open(hp, encoding='utf-8').read()
    tag = '<script src="./data.js"></script>'
    assert tag in h, 'index.html 里没有 data.js 的 script 标签'
    h = h.replace(tag, '<script>\n' + js + '</script>', 1)
    io.open(hp, 'w', encoding='utf-8').write(h)
    os.remove(p)
    print('index.html %d KB（data.js 已内联），剩余文件：%s'
          % (os.path.getsize(hp) // 1024, sorted(os.listdir(dst))))


if __name__ == '__main__':
    main()

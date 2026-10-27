#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 flash/mota50.swf 抽取全部中文文案（DoAction / DefineEditText 的字符串）。

SWF 是 CWS（zlib）；ActionPush 的字符串是「null 结尾的 UTF-8」，
所以按 0x00 切 DoAction 主体、只保留能严格 utf-8 解码且含 CJK 的段，足够干净。
"""
import zlib, sys, json, re

SRC = '/tmp/motarepo2/flash/mota50.swf'


def tags(body):
    i = 0
    n = len(body)
    while i + 2 <= n:
        code_len = body[i] | (body[i + 1] << 8)
        code, ln = code_len >> 6, code_len & 0x3F
        i += 2
        if ln == 0x3F:
            ln = int.from_bytes(body[i:i + 4], 'little'); i += 4
        data = body[i:i + ln]
        i += ln
        yield code, data


CJK = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')


def strings_of(data):
    out = []
    for seg in data.split(b'\x00'):
        if not seg:
            continue
        try:
            s = seg.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if CJK.search(s):
            out.append(s)
    return out


def main():
    raw = open(SRC, 'rb').read()
    body = zlib.decompress(raw[8:])
    nbits = body[0] >> 3
    hdr = (5 + 4 * nbits + 7) // 8 + 4          # RECT + frameRate(2) + frameCount(2)
    body = body[hdr:]
    all_s = []
    per_tag = []
    for code, data in tags(body):
        if code in (12, 59):                 # DoAction / DoInitAction
            ss = strings_of(data)
            if ss:
                per_tag.append(('DoAction', ss))
                all_s.extend(ss)
        elif code == 37:                     # DefineEditText
            ss = strings_of(data)
            if ss:
                per_tag.append(('EditText', ss))
                all_s.extend(ss)
    print('字符串 %d 条，来自 %d 个 tag' % (len(all_s), len(per_tag)))
    uniq = list(dict.fromkeys(all_s))
    print('去重后 %d 条' % len(uniq))
    json.dump(per_tag, open('/tmp/swf_texts.json', 'w'), ensure_ascii=False, indent=1)
    for s in uniq[:60]:
        print(repr(s))


if __name__ == '__main__':
    main()

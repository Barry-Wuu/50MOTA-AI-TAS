#!/usr/bin/env python3
"""把 MTower.class 的 twait(int)V 中的 `invokestatic Thread.sleep` 三字节改为 nop（无延迟省流版）。
只中和睡眠调用，其余字节码/异常表原样保留 —— 校验器看到的结构与原版一致，必过。
"""
import struct, shutil, os

SRC = '/tmp/motarepo2/08_Java_MTower08a/game/MTower.class'

def u2(b,o): return struct.unpack_from('>H', b, o)[0], o+2
def u4(b,o): return struct.unpack_from('>I', b, o)[0], o+4

def parse_cp(b, o, count):
    cp = [None]*count; i = 1
    while i < count:
        tag = b[o]; o += 1
        if tag == 1:
            ln, o = u2(b, o); cp[i] = ('utf8', b[o:o+ln].decode('utf-8','replace')); o += ln
        elif tag in (7,8,16,19,20):
            idx, o = u2(b, o); cp[i] = (tag, idx)
        elif tag == 15: o += 3; cp[i] = (tag,)
        elif tag in (3,4): o += 4; cp[i] = (tag,)
        elif tag in (5,6): o += 8; cp[i] = (tag,); i += 1
        elif tag in (9,10,11,12,17,18): o += 4; cp[i] = (tag,)
        else: raise ValueError(f'未知常量池 tag {tag} @ {o-1}')
        i += 1
    return cp, o

def utf8(cp, idx):
    e = cp[idx]
    return e[1] if e and e[0]=='utf8' else '?'

def skip_attributes(b, o):
    acnt, o = u2(b, o)
    for _ in range(acnt):
        _, o = u2(b, o)
        alen, o = u4(b, o)
        o += alen
    return o

def main():
    bak = SRC + '.orig'
    if not os.path.exists(bak):
        shutil.copy2(SRC, bak)
        print('备份 ->', bak)
    b = bytearray(open(SRC,'rb').read())
    assert b[:4] == b'\xca\xfe\xba\xbe', '不是 class 文件'
    o = 8
    cp_count, o = u2(b, o)
    cp, o = parse_cp(b, o, cp_count)
    o += 6
    ifc, o = u2(b, o); o += 2*ifc
    fcnt, o = u2(b, o)
    for _ in range(fcnt):
        o += 6
        o = skip_attributes(b, o)
    mcnt, o = u2(b, o)
    patched = 0
    for _ in range(mcnt):
        m_access, o = u2(b, o)
        name_idx, o = u2(b, o)
        desc_idx, o = u2(b, o)
        mname = utf8(cp, name_idx); mdesc = utf8(cp, desc_idx)
        acnt, o = u2(b, o)
        for _ in range(acnt):
            aname_idx, o = u2(b, o)
            alen, o = u4(b, o)
            aname = utf8(cp, aname_idx)
            if mname == 'twait' and mdesc == '(I)V' and aname == 'Code':
                p = o
                clen = struct.unpack_from('>I', b, p+4)[0]
                code_start = p + 8
                # 期望: 0:iload_1(1b) 1:i2l(85) 2:invokestatic(b8) ...
                head = bytes(b[code_start:code_start+3])
                print(f'  twait Code: len={clen} head={head.hex()} (期望 1b85b8)')
                if head == b'\x1b\x85\xb8':
                    # 把 iload_1(0) i2l(1) invokestatic(2-4) 共 5 字节全改 nop：
                    # 不推 long 也不调 sleep —— goto 18 处栈与原版一致（空），校验器结构不变
                    for k in range(5):
                        b[code_start+k] = 0x00
                    patched += 1
                    print('  [patch] iload_1;i2l;invokestatic sleep -> 5×nop（其余字节码原样）')
                else:
                    print('  !! 特征码不匹配，跳过')
            o += alen
    if patched:
        open(SRC,'wb').write(bytes(b))
        print(f'完成：写入 {SRC}')
    else:
        print('未 patch')

if __name__ == '__main__':
    main()

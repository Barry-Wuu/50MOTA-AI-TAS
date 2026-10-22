"""从 08_Java_MTower08a/game/MTower.class 的 javap 指令流提取“事件动态写入”的格子。

前置：
  cd 08_Java_MTower08a/game && javap -c -p MTower.class > mtower.jvm   (需 JDK 21)
用法：
  python3 tools/dynscan.py            # 生成 dyn_raw.json（动态物体/动态地形写入站点）
说明：
  匹配模式 = getfield map|mapObject ; push R ; aaload ; push C ; push V ; castore
  排除 loadMapData*/Initdata*（静态装载本身）、band5/slot9（引擎变量块）、band5/slot8（图鉴块）。
  本脚本只负责“哪些格会被运行时改写”，渲染叠加见 map_50f.png 的生成脚本。
"""
import re, json, collections
A='/workspace/f8fd4af0-b7d8-470f-bd1e-d5a9802c97d1/work/.artifacts'
L=[l.rstrip() for l in open(A+'/mtower.jvm',encoding='utf8',errors='replace')]
hd=[(i,l) for i,l in enumerate(L) if re.match(r'^  (?:public |private |protected |static |final |synchronized )*[A-Za-z_$][\w\.\$<>\[\]]* [A-Za-z_$][\w<>]*\(.*\);\s*$', l)]
def owner(i):
    o='?'
    for j,l in hd:
        if j<i: o=l
        else: break
    m=re.search(r' (\w+)\(',o); return m.group(1) if m else '?'
INS=re.compile(r'^\s+(\d+): (\w+)\s*(.*?)\s*$')
def at(i):
    m=INS.match(L[i]); return (m.group(2),m.group(3)) if m else (None,'')
def num(i):
    op,arg=at(i)
    if op in ('bipush','sipush'): return int(arg)
    if op=='iconst_m1': return -1
    if op and re.match(r'iconst_[0-5]$',op): return int(op[-1])
    return None
BASE={'loadMapData','loadMapData2','Initdata','Initdata2'}
obj=[]; ter=[]
for i,l in enumerate(L):
    if not re.search(r'\bcastore\b',l): continue
    op5,a5=at(i-5); op3,_=at(i-3)
    m=re.search(r'// Field (map|mapObject):',a5) if op5=='getfield' else None
    if not m or op3!='aaload': continue
    V,C,R=num(i-1),num(i-2),num(i-4)
    if None in (V,C,R) or not(0<=R<78 and 0<=C<130): continue
    mth=owner(i)
    if mth in BASE: continue
    band,y=divmod(R,13); slot,x=divmod(c:=C,13)
    slot,x=divmod(C,13)
    if band==5 and slot==9: continue          # 引擎变量块
    fl='0F' if (band,slot)==(5,1) else ('catalog' if (band,slot)==(5,8) else band*10+slot+1)
    if m.group(1)=='mapObject':
        if V!=0: obj.append({'floor':str(fl),'x':x,'y':y,'obj':V,'method':mth,'site':i})
    else:
        ter.append({'floor':str(fl),'x':x,'y':y,'to':V,'method':mth,'site':i})
json.dump({'obj':obj,'ter':ter},open(A+'/dyn_raw.json','w'),ensure_ascii=False)
print('动态物体写入站点:',len(obj),' 动态地形写入站点:',len(ter))
print('地形示例:',ter[:4])

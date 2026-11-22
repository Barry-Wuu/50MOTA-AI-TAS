"""TAS 脚本层展开器：把 merged_route_full.json 步骤展开成 Java 引擎忠实回放的按键脚本。
设计原则：菜单项在此层（TAS 脚本层）编码为真实按键序列，验证器 Headless8 只做忠实回放，
不检测 saidanFlag/itemFlag/yesnoNumber，不 hack 任何游戏状态。
三类菜单展开（均经真实引擎验证通过）：
  - 祭坛献金(14处)：面朝方向键(触发对话) + Enter(开菜单) + ↓×(sai-1) + Enter(确认)
  - 商店购物(7处)：面朝方向键(触发yes/no对话str=86) + Enter(选Yes)
  - 飞行珠传送(71处)：Enter(开道具栏选中obj26) + Enter×(层差)逐层飞 + ESC(退出选层模式)
    中间落点用 mota_core.FLY_LAND 预填（与 Java 引擎实测落点完全一致）。
用法: python3.11 expand_tas.py <limit_steps> <outprefix>
输出: emul_log/<outprefix>.keys + .csv，喂给: java Headless8 <runlog> <keys> <csv>
"""
import json, sys
BASE='/root/.codebuddy/artifact/2f8a7d30-9c21-4f0b-1d5b-ab5277f9b000/mota'
sys.path.insert(0,BASE+'/01_PC98原版_mtower/tools')
import mota_core as M
limit=int(sys.argv[1]); out=sys.argv[2]
s=json.load(open(BASE+'/09_TAS推演/merged_route_full.json',encoding='utf-8'))['steps']
DMAP={'↑':'u','↓':'d','←':'l','→':'r'}
keys=[]  # (char, f, x, y, note)
def emit(ch,f,x,y,note=''): keys.append((ch,f,x,y,note))

i=1  # 跳过 step0 起点快照
while i<limit and i<len(s):
    x=s[i]; l=x['l']; d=x['d']; f=x['f']; px=x['x']; py=x['y']
    if '购物' in l or ('花' in l and 'G' in l and '商店花费' not in l):
        # 商店购物：面朝商品触发 yes/no 对话(str=86) -> Enter 选 Yes 完成购买
        emit(DMAP.get(d,'u'),f,px,py,'面朝商店触发yes/no对话')
        emit('e',f,px,py,'Enter选Yes购买')
        emit('q',f,px,py,'ESC清购买成功消息框(否则后续面朝键被吞)')
        i+=1; continue
    if '商店花费' in l:
        emit(DMAP.get(d,'u'),f,px,py,'面朝祭坛触发对话')
        emit('e',f,px,py,'Enter打开祭坛菜单')
        sai=3 if '防御' in l else (2 if '攻击' in l else 1)
        for _ in range(sai-1): emit('d',f,px,py,'↓选sai→%d'%sai)
        emit('e',f,px,py,'Enter确认献金')
        emit('q',f,px,py,'ESC清献金成功消息框(str=1,否则下次献金/移动被吞)')
        i+=1; continue
    if '飞行之珠传送' in l and i>0:
        pf=s[i-1]['f']  # 起飞层
        delta=f-pf
        if delta==0:
            # 同层瞬移（昇華の翼式）：JSON 是坐标跳跃，Java 需另法；先保留单键占位
            emit(DMAP.get(d,'u'),f,px,py,'同层瞬移(待处理)')
            i+=1; continue
        # 逐层递推落点：第k次Enter后到 pf+k 层，落点 FLY_LAND[pf+k]
        n=abs(delta)
        emit('e',pf,s[i-1]['x'],s[i-1]['y'],'开道具栏选飞行珠')
        for k in range(1,n+1):
            nf=pf + (k if delta>0 else -k)
            lx,ly=M.FLY_LAND.get(nf,(px,py))
            emit('e',nf,lx,ly,'飞行第%d次Enter→%dF'%(k,nf))
        emit('q',f,px,py,'ESC退出选层模式')
        i+=1; continue
    emit(DMAP.get(d,'u'),f,px,py,'')
    i+=1

pfx=BASE+'/08_Java_MTower08a/game/emul_log/'+out
open(pfx+'.keys','w').write(''.join(k[0] for k in keys))
with open(pfx+'.csv','w',encoding='utf-8') as fh:
    for idx,(ch,f,x,y,note) in enumerate(keys,1):
        fh.write('%d,%d,%d,%d\n'%(idx,f,x,y))
print('展开 step1..%d -> %d 按键'%(limit-1,len(keys)))
for k in keys:
    if k[4] and ('飞行' in k[4] or '飞行珠' in k[4] or '道具' in k[4]):
        print('  %s @%dF(%d,%d) %s'%(k[0],k[1],k[2],k[3],k[4]))

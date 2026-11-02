# -*- coding: utf-8 -*-
"""指南 2区(11F-20F) 路线抽象可行性模拟（PC-98 真值模型）
怪物四维来自 magic_tower1_monsters.csv；药水 obj66=+100, obj76=+400;
祭坛逐区缩放(936c705)：12F 区=1 -> ATK+4/DEF+8, HP+(k+1)*100;
宝石 2区：obj80 红晶 ATK+2, obj83 蓝晶 DEF+2。
战斗：回合=ceil(怪HP/(我ATK-怪DEF)); 扣血=max(0,怪ATK-我DEF)*(回合-1)。
"""
import math
MON = {  # id: (hp, atk, dfn)
 7:(35,38,3),   # 小蝙蝠
 8:(60,32,8),   # 初级法师
 45:(130,60,3), # 大史莱姆
 46:(100,95,30),# 高级法师(上級僧侣)
 47:(60,100,8), # 大蝙蝠
 48:(260,85,5), # 兽人
 49:(320,120,15),# 兽人武士
 56:(20,100,68),# 石头人
 5:(35,18,1),   # 绿史莱姆
 9:(50,42,6),   # 骷髅人
 10:(55,52,12), # 骷髅士兵
 59:(444,199,66),# 吸血鬼
}
def dmg(oid, A, D, x2=1):
    hp,atk,dfn = MON[oid]
    per = A*x2 - dfn
    if per <= 0: return None  # 打不动
    n = math.ceil(hp/per)
    return max(0, atk-D)*(n-1)

# 从 11F 入口开始（1区引擎验证：HP1014 A27 D31 钥4/0/0）
H,A,D = 1014,27,31
ky,kb,kr = 4,0,0
G = 0
LOG=[]
def fight(oid, tag):
    global H
    d = dmg(oid,A,D)
    LOG.append(f"{tag}: F{oid} dmg={d} (A{A}/D{D})")
    H -= d
def potion(v, tag):
    global H
    H += v; LOG.append(f"{tag}: +{v} -> HP{H}")
def altar(pol):
    global H,A,D,G,k
    # 12F 祭坛：区=1 -> ATK+4 / DEF+8 / HP+(k+1)*100
    if pol=='atk': A+=4
    elif pol=='dfn': D+=8
def gem(pol):
    global A,D
    if pol=='atk': A+=2
    else: D+=2

# 指南 line207-239 序列
# 1. 11F: 直接向右打蝙蝠上楼
fight(7,'11F 蝙蝠')
# 2. 12F: 左蝙蝠, 祭坛2防1攻, 蝙蝠上楼
fight(7,'12F 蝙蝠')
altar('dfn'); altar('dfn'); altar('atk')   # 2防1攻 -> A31/D47
fight(7,'12F 蝙蝠2')
# 3. 13F: 上楼(无战)
# 4. 14F: 黄门, 大史莱姆, 黄门, 暗道, 血瓶, 回11F
ky-=1  # 黄门
fight(45,'14F 大史莱姆')
ky-=1  # 黄门
potion(66,'14F 血瓶')  # 红药+100
# 5. 11F: 10F梯左侧黄门, 大史莱姆, 回14F
ky-=1
fight(45,'11F 大史莱姆')
# 6. 15F: 黄门蝙蝠, 两道黄门大蝙蝠, 黄门大史莱姆, 小偷
ky-=1; fight(7,'15F 蝙蝠')
ky-=2; fight(47,'15F 大蝙蝠')
ky-=1; fight(45,'15F 大史莱姆')
# 7. 12F: 吃2血瓶, 黄门兽人拿钥匙, 上16F
potion(66,'12F 血瓶1'); potion(66,'12F 血瓶2')
ky-=1; fight(48,'12F 兽人'); ky+=1  # 拿钥匙
print('--- 到达 16F 前 ---')
print(f'HP={H} A={A} D={D} 黄钥={ky} 蓝钥={kb} 红钥={kr}')
LOG.clear()  # 以下继续模拟16F/17F 但单独打印

# ==== 继续 16F → 20F（HP 跟踪，钥匙粗估）====
def fight2(oid, tag):
    global H
    d = dmg(oid,A,D)
    LOG.append(f"{tag}: F{oid} dmg={d} (A{A}/D{D})")
    H -= d
def gem2(pol):
    global A,D
    if pol=='atk': A+=2
    else: D+=2
def altar2():
    global A
    A+=4  # 12F 祭坛攻

# 8. 16F: 蓝门(蓝钥), 血瓶+钥匙, 黄门, 黄门, 老头, 大史莱姆, 暗道, 钥匙+红蓝宝石+血瓶
kb-=1  # 蓝门
potion(76,'16F 蓝药+400'); ky+=1  # 拿钥匙
ky-=1  # 黄门
ky-=1  # 黄门
fight2(45,'16F 大史莱姆')
gem2('atk'); gem2('dfn')  # 红蓝宝石 -> A33/D49
potion(66,'16F 红药+100')
# 9. 17F: 大蝙蝠, 血瓶, 黄门, 4初级卫兵(不伤), 银剑A+20
fight2(47,'17F 大蝙蝠')
potion(66,'17F 红药+100')
ky-=1  # 黄门
A+=20  # 銀の剣
# 10. 12F: 祭坛攻
altar2()  # A57
# 11. 8F: 2黄门, 骷髅/骷髅战士, 血瓶+钥匙
ky-=2; fight2(9,'8F 骷髅人'); fight2(10,'8F 骷髅士兵')
potion(66,'8F 红药+100'); ky+=1
# 12. 11F: 大蝙蝠, 蓝门血瓶, 2高级法师, 银盾D+20
fight2(47,'11F 大蝙蝠')
kb-=1; potion(76,'11F 蓝药+400')
fight2(46,'11F 高级法师'); fight2(46,'11F 高级法师2')
D+=20  # 銀の盾
# 13. 12F: 兽人, 黄门大史莱姆, 血瓶+钥匙+蓝宝石
fight2(48,'12F 兽人'); ky-=1; fight2(45,'12F 大史莱姆')
potion(66,'12F 红药+100'); ky+=1; gem2('dfn')  # D71
# 14. 15F: 黄门兽人, 蓝宝石
ky-=1; fight2(48,'15F 兽人'); gem2('dfn')  # D73
# 15. 11F: 大蝙蝠, 大史莱姆, 血瓶+钥匙, 黄门兽人, 黄门红宝石
fight2(47,'11F 大蝙蝠'); fight2(45,'11F 大史莱姆')
potion(66,'11F 红药+100'); ky+=1
ky-=1; fight2(48,'11F 兽人'); ky-=1; gem2('atk')  # A59
# 16. 6F: 初级法师, 钥匙
fight2(8,'6F 初级法师'); ky+=1
# 17. 12F: 黄门高级法师, 血瓶, 兽人, 黄门高级法师, 钥匙+红宝石
ky-=1; fight2(46,'12F 高级法师'); potion(76,'12F 蓝药+400')
fight2(48,'12F 兽人'); ky-=1; fight2(46,'12F 高级法师2')
ky+=1; gem2('atk')  # A61
# 18. 14F: 大史莱姆, 黄门兽人, 血瓶, 大蝙蝠, 黄门兽人武士, 血瓶+钥匙+蓝宝石
fight2(45,'14F 大史莱姆'); ky-=1; fight2(48,'14F 兽人')
potion(66,'14F 红药+100'); fight2(47,'14F 大蝙蝠')
ky-=1; fight2(49,'14F 兽人武士'); potion(66,'14F 红药+100'); ky+=1; gem2('dfn')  # D75
# 19. 17F: 大蝙蝠, 血瓶, 黄门2兽人, 2兽人武士, 血瓶+钥匙+红蓝宝石
fight2(47,'17F 大蝙蝠'); potion(66,'17F 红药+100')
ky-=1; fight2(48,'17F 兽人'); fight2(48,'17F 兽人2')
fight2(49,'17F 兽人武士'); fight2(49,'17F 兽人武士2')
potion(66,'17F 红药+100'); ky+=1; gem2('atk'); gem2('dfn')  # A63/D77
print('--- 到 17F 二访完成 ---')
print(f'HP={H} A={A} D={D} 黄钥={ky} 蓝钥={kb} 红钥={kr}')
for l in LOG: print(' ',l)

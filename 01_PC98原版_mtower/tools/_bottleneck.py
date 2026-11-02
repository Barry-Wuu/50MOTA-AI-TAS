# -*- coding: utf-8 -*-
"""十字架前兽人武士瓶颈精确核算（PC-98 真值）。"""
import math
def dmg(hp,atk,dfn,A,D,x2=1):
    per=A*x2-dfn
    if per<=0: return None
    n=math.ceil(hp/per)
    return max(0,atk-D)*(n-1)
# 兽人武士 obj49 = 320/120/15
print('兽人武士 obj49 320/120/15')
for A,D,tag in [(61,75,'14F段/17F段(宝石前)'),(63,77,'17F段(宝石前,略高)'),(66,80,'17F(宝石后=指南A66/D80)'),(70,84,'拿十字架后(指南18F-19F A70)')]:
    d=dmg(320,120,15,A,D)
    print(f'  @A{A}/D{D} [{tag}]: 战损/只 = {d}  回合={math.ceil(320/(A-15))}')
print()
# 十字架后（x2=2 对 48/49）
for A,D,tag in [(70,84,'19F拿十字架后兽人武士'),(78,90,'20F决战前')]:
    d=dmg(320,120,15,A,D,x2=2)
    print(f'  十字架后 @A{A}/D{D} [{tag}]: 战损/只 = {d}  回合={math.ceil(320/(A*2-15))}')
print()
# 14F 蓝晶路线：14F 蓝晶 obj83 (5,1)；17F 红/蓝晶 obj80(11,1) obj83(9,1)
print('关键属性差：PC-98 11F入口 HP1014 A27 D31；中文版指南(旧模型CSV) 11F入口 HP1845 A27 D37')
print('  → PC-98 2区入口 HP 比中文版低 ~831，DEF 低 6 → 全程战损更高，兽人武士段更紧')

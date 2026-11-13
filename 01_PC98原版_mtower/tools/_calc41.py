# -*- coding: utf-8 -*-
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mota_core as M

def battle(o, atk, dfn):
    hp, a, d, g = M.oatr(o,10), M.oatr(o,11), M.oatr(o,12), M.oatr(o,13)
    per = atk - d
    turns = math.ceil(hp/per)
    loss = max(a-dfn,0)*(turns-1)
    return loss, g, hp, a, d, turns, per

for o in (58,99,100,97,98):
    if o==58: nm='魔導師'; 
    elif o==99: nm='魔術師A'
    elif o==100: nm='魔術師B'
    elif o==97: nm='吸血蝙蝠'
    else: nm='Kスライム'
    r = battle(o, 222, 206)
    print('obj%-3d %-8s hp=%-5d atk=%-4d def=%-4d turns=%d per=%d  loss=%d gold=%d' % (o,nm,r[2],r[3],r[4],r[5],r[6],r[0],r[1]))

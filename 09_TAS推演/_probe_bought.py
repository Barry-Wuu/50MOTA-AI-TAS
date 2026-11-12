# -*- coding: utf-8 -*-
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manual
manual.execute(manual.PLAN, verbose=False)
W = manual.W
print('bought=', W.bought)
print('7F(6,1) obj=', W.at(7, 6, 1), 'cleared?', (7, 6, 1) in W.cleared)
print('6F(8,4) obj=', W.at(6, 8, 4), 'cleared?', (6, 8, 4) in W.cleared)
print('G=', W.hero.gold, 'keys=', W.hero.keys)

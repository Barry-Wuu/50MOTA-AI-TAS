# -*- coding: utf-8 -*-
import csv, io
SRC = r'D:/B++/WorkBuddy/mota_tas_tmp2/repo/01_PC98原版_mtower/'
rows = list(csv.DictReader(io.open(SRC + '魔塔1_route_1F到21F.csv', encoding='utf-8')))
for i in list(range(1238, 1250)) + list(range(2240, 2262)):
    r = rows[i]
    print(i + 1, r['step'], r['floor'], r['x'], r['y'], 'hp', r['hp'], 'atk', r['atk'], 'def', r['def'],
          'g', r['gold'], r['ky'], r['kb'], r['kr'], '|', r['event'][:70])
print('--- last row ---')
print(rows[-1])

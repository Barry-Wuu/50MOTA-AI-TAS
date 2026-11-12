# -*- coding: utf-8 -*-
"""Check dyn_raw.json for 34F key cells: static vs event-triggered."""
import json, os
sys_path = r'D:\B++\WorkBuddy\mota_tas_tmp2\repo\01_PC98原版_mtower'
# find artifacts dir
for root, dirs, files in os.walk(sys_path):
    if 'dyn_raw.json' in files:
        art = root
        break
print('ART dir:', art)
dyn = json.load(open(os.path.join(art, 'dyn_raw.json')))
# keys of interest
import re
for k, v in dyn.items():
    ks = str(k)
    # 34F cells
    pass
# inspect structure
print('dyn keys sample:', list(dyn.keys())[:10])

"""仅求进入 4F（obj19 不可踩修正后）"""
import json, collections, csv
import mk_enter as E

res = E.astar(4, cap=1500000)
assert res, '4F 搜索失败'
path, acts, nodes, cost = res
w, rows = E.replay(acts)
assert w is not None and w.hero.f == 4, '复验失败'
per = collections.Counter(r[1] for r in rows)
enter_step = next(r[0] for r in rows if r[1] == 4)
KS = {(0,-1):'8',(0,1):'2',(-1,0):'4',(1,0):'6'}
keys = ''.join(KS[d] for d in acts)
out = {'steps': len(rows), 'enter_step': enter_step,
       'per_floor_steps': {str(k):v for k,v in sorted(per.items())},
       'final_cell':[int(w.hero.x),int(w.hero.y)], 'HP':int(w.hero.hp),'ATK':int(w.hero.atk),
       'DEF':int(w.hero.dfn),'GOLD':int(w.hero.gold),'keys_y':int(w.hero.keys['y']),
       'nodes':nodes, 'keys':keys,
       'events':[r[10] for r in rows if ('剧本' in r[10] or '掉血' in r[10])]}
with open('route_enter_4f.csv','w',newline='',encoding='utf8') as fh:
    wr=csv.writer(fh)
    wr.writerow(['step','floor','x','y','HP','ATK','DEF','GOLD','黄钥匙','蓝钥匙','本步事件'])
    wr.writerows(rows)
open('keys_enter_4f.txt','w').write(keys)
json.dump({'4':out}, open('route_enter_4f_summary.json','w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))

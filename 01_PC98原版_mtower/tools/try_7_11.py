import sys, mota_core as M

def start_at(hp, y=1, b=1, r=0, gold=0, atk=20, dfn=10):
    w = M.World.new(event_mode='on_entry', trap_mode='apply')
    h = w.hero
    h.f, h.x, h.y = 7, 11, 10
    h.hp, h.atk, h.dfn, h.gold = hp, atk, dfn, gold
    h.keys['y'], h.keys['b'], h.keys['r'] = y, b, r
    w.trap_done = True; w.flag3F = 1        # 假定 3F 剧本已过
    w.applied_events.clear()
    w.apply_floor_events(7)
    return w

def run(hp, max_states):
    st = start_at(hp)
    r = M.plan(lambda f,x,y: f==11, start=st, max_states=max_states, goal_cell=(11,6,10))
    if r is None:
        print(f"HP={hp}: 图不可达(无解)"); return
    if isinstance(r,tuple) and r and r[0]=='cap':
        print(f"HP={hp}: 撞状态上限 {r[1]}"); return
    w,path = r
    print(f"HP={hp}: 成功! 步数={len(path)-1} 余血={w.hero.hp} ATK={w.hero.atk} DEF={w.hero.dfn} 钥匙={dict(w.hero.keys)} GOLD={w.hero.gold} 终点={w.hero.f}F({w.hero.x},{w.hero.y})")
    # 回溯掉血/事件
    print("  caveats:", w.caveats)
    for p in path:
        print("   ", p)

if __name__=='__main__':
    hp=int(sys.argv[1]) if len(sys.argv)>1 else 2000
    ms=int(sys.argv[2]) if len(sys.argv)>2 else 800000
    run(hp, ms)

# -*- coding: utf-8 -*-
"""10 分钟后自动部署最新 toy_final 到 B 站 Toy（一次性后台任务）。"""
import io, json, os, subprocess, sys, time

PY = r'D:/B++/Py313/python.exe'
TOY = r'D:/B++/WorkBuddy/tools/toy/toy.exe'
HERE = os.path.dirname(os.path.abspath(__file__))
TOID = '54630033656832'
SLUG = 'mota50-route'

def log(msg):
    print('[%s] %s' % (time.strftime('%H:%M:%S'), msg), flush=True)

def toy_status():
    """返回 mota50-route 的 status；解析失败返回 None。"""
    r = subprocess.run([TOY, 'mylist', '--json'], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        items = d.get('list', d) if isinstance(d, dict) else d
        for it in items:
            if SLUG in it.get('url', ''):
                return it.get('status')
    except Exception as e:
        log('mylist 解析失败: %s' % e)
    return None

log('后台部署任务启动，等待 10 分钟…')
time.sleep(600)

# 等当前审核中版本过审（最多 20 分钟）
for i in range(20):
    st = toy_status()
    log('第 %d 次状态检查: %s' % (i + 1, st))
    if st == 'published':
        break
    if st == 'auditing':
        time.sleep(60)
        continue
    # rejected / None: 直接尝试部署
    break

log('执行 toy update …')
r = subprocess.run([TOY, 'update', TOID, 'toy_final', '--visibility', 'public', '--yes'],
                   cwd=HERE, capture_output=True, text=True)
out = (r.stdout or '') + (r.stderr or '')
log('update rc=%d' % r.returncode)
log(out.strip()[-1500:])

# 若遇 307013（审核中），再等过审后重试一次
if '307013' in out:
    log('遇到 307013，等待过审后重试一次…')
    for i in range(20):
        st = toy_status()
        log('重试前状态: %s' % st)
        if st == 'published':
            break
        time.sleep(60)
    r = subprocess.run([TOY, 'update', TOID, 'toy_final', '--visibility', 'public', '--yes'],
                       cwd=HERE, capture_output=True, text=True)
    out = (r.stdout or '') + (r.stderr or '')
    log('重试 update rc=%d' % r.returncode)
    log(out.strip()[-1500:])

log('后台部署任务结束')

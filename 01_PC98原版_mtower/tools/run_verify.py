"""实机验证「进入 2F/3F/4F/5F / 取 5F 铁剑 最少步数」：按 keys_<tag>.txt 逐步执行，
在每次「层切换 / 踩中 3F 扒装剧本」的步号自动截图，供人工/程序确认塔层号。

用法（在你本机 np2kai + Xvfb :99 + xdotool 环境下）：
    python3 run_verify.py tools/keys_enter_4f.txt [起始步号]
脚本会自动读取同 tag 的 route_<tag>.csv 取出层切换/剧本步号作为检查点截图。
"""
import sys, os, time, csv, subprocess
sys.path.insert(0, '/tmp')            # nat.py / walk3.py 所在
import nat, walk3

KEYS = {'8': 'U', '2': 'D', '4': 'L', '6': 'R'}


def dialog(img):
    reg = img[235:365, 155:485]
    return ((reg[:, :, 0] < 120) & (reg[:, :, 1] < 120) & (reg[:, :, 2] < 120)).mean() > 0.90


def checkpoints_from_csv(csv_path, keys_len):
    """取 route csv 中楼层变化或剧本/楼梯触发的步号作检查点（去重排序，且 <= 按键数）。"""
    cps = set()
    prev_f = None
    try:
        with open(csv_path) as fh:
            rd = csv.reader(fh)
            next(rd)
            for r in rd:
                step = int(r[0]); f = int(r[1]); ev = r[11] if len(r) > 11 else ''
                if f != prev_f:
                    cps.add(step); prev_f = f
                if '剧本' in ev or '楼梯' in ev:
                    cps.add(step)
    except FileNotFoundError:
        pass
    return sorted(c for c in cps if 1 <= c <= keys_len)


def run(keys, start=1, checkpoints=None):
    log = []
    for i, ch in enumerate(keys, 1):
        if i < start:
            continue
        p0 = walk3.get_pos()
        img = nat.load('/tmp/g3.png')
        if dialog(img):                       # 剧本/对话：按 Return 推进
            walk3.click_win()
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'Return'],
                           env=walk3.ENV, check=False)
            time.sleep(0.8)
            log.append((i, 'DIALOG', 'Return'))
        for _ in range(3):                    # 单步：允许重试（门/剧本会挡）
            walk3.press(KEYS[ch])
            p1 = walk3.get_pos()
            img2 = nat.load('/tmp/g3.png')
            if dialog(img2):
                walk3.click_win()
                subprocess.run(['xdotool', 'key', '--clearmodifiers', 'Return'],
                               env=walk3.ENV, check=False)
                time.sleep(0.8)
                p1 = walk3.get_pos()
            if p1 != p0:
                break
        log.append((i, ch, p1))
        print(f'step {i:3d} {ch} {p0} -> {p1}', flush=True)
        if checkpoints and i in checkpoints:
            nat.shot(f'/tmp/enter_{i}.png')
            print(f'  >> 检查点 {i} 已截图', flush=True)
    return log


if __name__ == '__main__':
    keys_file = sys.argv[1]
    st = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    keys = open(keys_file).read().strip()
    csv_path = os.path.splitext(keys_file)[0].replace('keys_', 'route_') + '.csv'
    cps = checkpoints_from_csv(csv_path, len(keys))
    print(f'按键数={len(keys)} 检查点(层切换/剧本)={cps}', flush=True)
    run(keys, st, cps)

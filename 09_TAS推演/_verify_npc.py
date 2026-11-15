import asyncio, os


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        pg = await b.new_page(viewport={'width': 1400, 'height': 1000})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        fp = os.path.abspath('toy_final/index.html').replace(os.sep, '/')
        await pg.goto('file:///' + fp)
        await pg.wait_for_timeout(800)

        # 遍历所有楼层，统计 npcmark 数量与 data-npc 名字
        names = await pg.evaluate("""() => {
          const set = {};
          // 直接读模板里的 NPC_DLG 键（在 IIFE 内，只能从 DOM 侧看）
          const marks = document.querySelectorAll('.npcmark');
          marks.forEach(m => { set[m.dataset.npc] = 1; });
          return Object.keys(set);
        }""")
        print('当前层 npcmark 名字:', names)

        # 逐层切换找到有 NPC 的层
        got = None
        for idx in range(0, 6800, 37):
            n = await pg.evaluate("""(i) => {
              const s = D.steps[i];
              return s ? s.f : null;
            }""", idx)
            if n is None:
                continue
            await pg.evaluate("""(i) => {
              const sl = document.getElementById('slider');
              sl.value = i;
              sl.dispatchEvent(new Event('input', {bubbles: true}));
            }""", idx)
            await pg.wait_for_timeout(60)
            cnt = await pg.evaluate("() => document.querySelectorAll('.npcmark').length")
            if cnt:
                got = (idx, n, cnt)
                break
        print('找到 NPC 层:', got)

        if got:
            # 悬停验证 tooltip 能否弹出（键名匹配成功才显示）
            box = await pg.evaluate("""() => {
              const m = document.querySelector('.npcmark');
              const r = m.getBoundingClientRect();
              return [r.x + r.width / 2, r.y + r.height / 2, m.dataset.npc];
            }""")
            await pg.mouse.move(box[0], box[1])
            await pg.wait_for_timeout(400)
            tip = await pg.evaluate("""() => {
              const t = document.getElementById('npctip');
              return {disp: getComputedStyle(t).display, txt: (t.textContent || '').replace(/\\s+/g, ' ').slice(0, 80)};
            }""")
            print('tooltip:', box[2], '->', tip)
        print('errs:', errs or 'none')
        await b.close()

asyncio.run(main())

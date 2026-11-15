import asyncio, os

JS_SET = """(i) => {
  const sl = document.getElementById('slider');
  sl.value = i;
  sl.dispatchEvent(new Event('input', {bubbles: true}));
}"""

JS_STAT = """() => {
  const cl = document.getElementById('consumeLayer');
  const cs = [...cl.querySelectorAll('.cons')];
  return {
    painted: cs.length,
    plain: cs.filter(x => x.className.trim() === 'cons').length,
    dyn: document.getElementById('dynLayer').querySelectorAll('.dynmk').length,
    fl: document.getElementById('floorname').textContent,
    pos: document.getElementById('posline').textContent.replace(/\\s+/g, ' ')
  };
}"""


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

        info = await pg.evaluate("""() => {
          const idx = D.steps.findIndex(s => (s.l||'').includes('超级镐'));
          const f37 = D.steps.map((s,i)=>({i,s})).filter(o=>o.s.f===37).map(o=>o.i);
          const k3 = D.steps.map((s,i)=>({i,s})).filter(o=>o.s.f===37 && (o.s.l||'').includes('击杀 obj91'));
          return {total: D.steps.length, pickIdx: idx, pickStep: D.steps[idx].i,
                  f37First: f37[0], f37Last: f37[f37.length-1], f37Count: f37.length,
                  knightSteps: k3.map(o=>o.s.i)};
        }""")
        print('信息:', info)

        for tag, idx in (('超级镐后 42 步末', info['f37Last'] - 9),
                         ('三怪打完', info['f37Last'])):
            await pg.evaluate(JS_SET, idx)
            await pg.wait_for_timeout(350)
            print(tag, '->', await pg.evaluate(JS_STAT))
            el = await pg.query_selector('#mapbox')
            await el.screenshot(path='_shot_37f_%s.png' % ('sweep' if '42' in tag else 'end'))

        # 45F 是否从 37F 直飞进入
        nxt = await pg.evaluate("""() => {
          const i = D.steps.findIndex(s => s.f===45);
          return {idx:i, step:D.steps[i].i, l:D.steps[i].l, x:D.steps[i].x, y:D.steps[i].y};
        }""")
        print('先进 45F:', nxt)
        print('JS errors:', errs or 'none')
        await b.close()

asyncio.run(main())

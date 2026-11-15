import asyncio, os

JS_STAT = """() => ({
  badge: document.getElementById('dirbadge').textContent,
  pos: document.getElementById('posline').textContent.replace(/\\s+/g, ' '),
  hero: (document.getElementById('heroImg').src || '').slice(0, 26)
})"""


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        pg = await b.new_page(viewport={'width': 1400, 'height': 1000})
        fp = os.path.abspath('toy_final/index.html').replace(os.sep, '/')
        await pg.goto('file:///' + fp)
        await pg.wait_for_timeout(800)

        info = await pg.evaluate("""() => {
          const i = D.steps.findIndex(s => (s.l || '').indexOf('中心飞行器：41F') >= 0);
          const s = D.steps[i];
          const j = D.steps.findIndex(x => (x.l || '').indexOf('中心飞行器：45F') >= 0);
          return {i41: i, s41: [s.i, s.f, s.x, s.y, s.d], i45: j,
                  s45: [D.steps[j].i, D.steps[j].f, D.steps[j].x, D.steps[j].y, D.steps[j].d]};
        }""")
        print('41F 飞行步:', info['s41'], ' 45F 飞行步:', info['s45'])

        for idx, name in ((info['i41'], '_shot_41f_wing.png'), (info['i45'], '_shot_45f_wing.png')):
            await pg.evaluate("""(i) => {
              const sl = document.getElementById('slider');
              sl.value = i;
              sl.dispatchEvent(new Event('input', {bubbles: true}));
            }""", idx)
            await pg.wait_for_timeout(400)
            print(idx, await pg.evaluate(JS_STAT))
            el = await pg.query_selector('#mapbox')
            await el.screenshot(path=name)
        await b.close()

asyncio.run(main())

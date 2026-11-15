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
    n: cs.length,
    plain: cs.filter(x => x.className.trim() === 'cons').length,
    dyn: document.getElementById('dynLayer').querySelectorAll('.dynmk').length,
    fl: document.getElementById('floorname').textContent
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
        await pg.wait_for_timeout(700)
        for idx in (6073, 6100, 6160):
            await pg.evaluate(JS_SET, idx)
            await pg.wait_for_timeout(350)
            print(idx, await pg.evaluate(JS_STAT))
        await pg.screenshot(path='_shot_37f_pick.png')
        print('errs', errs or 'none')
        await b.close()

asyncio.run(main())

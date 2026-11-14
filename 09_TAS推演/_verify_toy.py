import asyncio, os
async def check():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        pg = await b.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        fp = os.path.abspath("toy_final/index.html").replace("\\", "/")
        await pg.goto("file:///" + fp)
        await pg.wait_for_timeout(1000)
        total = await pg.eval_on_selector("#stepLabel", "el => el.textContent")
        print("Step label:", total)
        counts = await pg.evaluate("""() => {
            return {
                f1: D.steps.filter(s=>s.f===1).length,
                f27: D.steps.filter(s=>s.f===27).length,
                f15: D.steps.filter(s=>s.f===15).length,
                total: D.steps.length
            };
        }""")
        print("Counts:", counts)
        print("JS errors:", errors if errors else "none")
        await b.close()
asyncio.run(check())

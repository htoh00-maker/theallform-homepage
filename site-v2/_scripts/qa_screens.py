"""site-v2 화면 점검용 스크린샷 (데스크톱 1440x900, 휴대폰 390x844)."""
import os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(HERE, "..", "index.html").replace("\\", "/")
OUT = os.path.join(HERE, "..", "_qa")
IDS = ["top", "wide-brick", "wide-tile", "design-block", "colors", "cutting", "projects", "contact"]
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp, mobile in [("desktop", {"width": 1440, "height": 900}, False), ("mobile", {"width": 390, "height": 844}, True)]:
        pg = b.new_page(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(1500)
        for i, sid in enumerate(IDS):
            pg.evaluate(f"document.getElementById('{sid}').scrollIntoView({{behavior:'instant'}})")
            pg.wait_for_timeout(1300)
            pg.screenshot(path=os.path.join(OUT, f"{name}_{i+1:02d}_{sid}.png"))
        if mobile:
            pg.evaluate("document.getElementById('top').scrollIntoView({behavior:'instant'})"); pg.wait_for_timeout(600)
            pg.click(".gnb-menu"); pg.wait_for_timeout(800)
            pg.screenshot(path=os.path.join(OUT, f"{name}_09_menu.png"))
        # 가로 넘침 검사
        ow = pg.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        broken = pg.evaluate("[...document.images].filter(i=>i.complete && i.naturalWidth===0).map(i=>i.src)")
        print(name, "errors:", errs, "horizontal overflow:", ow, "broken imgs:", broken)
        pg.close()
    b.close()

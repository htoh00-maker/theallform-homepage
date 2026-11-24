"""site-v2 하위 페이지 점검 — 전체 길이 스크린샷 (데스크톱 1440x900, 휴대폰 390x844) + 오류 검사.
실행: python qa_subpages.py [페이지이름 ...]   결과: ../_qa/sub_*.png
"""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "_qa")
PAGES = sys.argv[1:] or ["products", "products-wide-brick", "products-wide-tile", "products-design-block",
                         "products-cutting", "projects", "about", "resources", "qna"]

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp, mobile in [("desktop", {"width": 1440, "height": 900}, False), ("mobile", {"width": 390, "height": 844}, True)]:
        for page_name in PAGES:
            pg = b.new_page(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("file:///" + os.path.join(ROOT, page_name + ".html").replace("\\", "/"))
            # 지연 로딩 사진과 등장 효과가 모두 뜨도록 끝까지 천천히 내려갔다 올라옴
            h = pg.evaluate("document.documentElement.scrollHeight")
            for y in range(0, h, 500):
                pg.evaluate(f"window.scrollTo(0, {y})"); pg.wait_for_timeout(60)
            pg.wait_for_timeout(800)
            pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(900)
            pg.screenshot(path=os.path.join(OUT, f"sub_{name}_{page_name}_top.png"))
            pg.screenshot(path=os.path.join(OUT, f"sub_{name}_{page_name}_full.png"), full_page=True)
            ow = pg.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            broken = pg.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.src)")
            print(name, page_name, "errors:", errs, "overflow:", ow, "broken:", broken)
            pg.close()
    b.close()

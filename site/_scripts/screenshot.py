import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8791/"
OUT = r"F:\OHT\Ai\LLM Wiki Ux\Project\homepage\site\_scripts\shots"
import os
os.makedirs(OUT, exist_ok=True)

jobs = [
    ("index.html", "home_desktop", 1440, 900, True),
    ("products.html", "products_desktop", 1440, 900, True),
    ("products-cutting.html", "cutting_desktop", 1440, 900, True),
    ("index.html", "home_mobile", 390, 844, True),
    ("products-cutting.html", "cutting_mobile", 390, 844, True),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for path, name, w, h, full in jobs:
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(BASE + path, wait_until="networkidle")
        page.screenshot(path=os.path.join(OUT, name + ".png"), full_page=full)
        page.close()
    browser.close()
print("done")

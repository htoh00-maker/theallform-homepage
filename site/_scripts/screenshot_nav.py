from playwright.sync_api import sync_playwright
import os

OUT = r"F:\OHT\Ai\LLM Wiki Ux\Project\homepage\site\_scripts\shots"
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://localhost:8791/index.html", wait_until="networkidle")
    page.click(".nav-toggle")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(OUT, "mobile_nav_open.png"), full_page=True)
    browser.close()
print("done")

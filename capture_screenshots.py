"""Capture screenshots for NIR documentation."""

from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"C:\Users\janap\Downloads\resume-ai-demo\screenshots")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:8000"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        page.goto(BASE)
        page.wait_for_timeout(800)
        page.screenshot(path=str(OUT / "01-zhakt-akparat.png"), full_page=True)

        page.click("text=Келесі")
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / "02-tazhiribe.png"), full_page=True)

        page.click("text=Келесі")
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT / "03-dagdylar.png"), full_page=True)

        page.click("text=Келесі")
        page.wait_for_timeout(400)
        page.click("text=AI генерациялау")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(OUT / "04-ai-taldau.png"), full_page=True)

        page.goto(f"{BASE}/docs")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUT / "05-swagger-api.png"), full_page=True)

        browser.close()
        print("Saved screenshots to", OUT)


if __name__ == "__main__":
    main()

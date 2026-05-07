import argparse

from playwright.sync_api import sync_playwright


def screenshot_page(url: str, out: str) -> None:
    print("Opening browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state={"cookies": [], "origins": []},
        )
        page = context.new_page()

        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        print("Taking screenshot...")
        page.screenshot(path=out, full_page=True)
        browser.close()

    print(f"Screenshot saved to {out}")


def main():
    parser = argparse.ArgumentParser(description="Screenshot a live page via Playwright")
    parser.add_argument("--url", required=True, help="URL of the page to screenshot")
    parser.add_argument("--out", required=True, help="Output path for PNG file")
    args = parser.parse_args()

    screenshot_page(args.url, args.out)


if __name__ == "__main__":
    main()

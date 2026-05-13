import argparse
import json
from playwright.sync_api import sync_playwright

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",required=True)
    parser.add_argument("--out", default="page_inventory.json")
    args = parser.parse_args()

    with sync_playwright() as p:    
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(args.url,wait_until="networkidle")
        print("Page title:", page.title())
        browser.close()

if __name__ == "__main__":
    main()
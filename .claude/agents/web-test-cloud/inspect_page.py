import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", default="page_inventory.json")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(args.url, wait_until="networkidle")
        title = page.title()
        aria_tree = page.aria_snapshot()
        browser.close()

    inventory = {"url": args.url, "title": title, "accessibility_tree": aria_tree}
    Path(args.out).write_text(json.dumps(inventory, indent=2))
    print(f"Title: {title}")
    print(f"Inventory written to {args.out}")


if __name__ == "__main__":
    main()
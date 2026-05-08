import argparse
import os
import re
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()


def parse_figma_url(url: str) -> tuple[str, str]:
    match = re.search(r"figma\.com/(?:design|proto)/([^/?]+)", url)
    if not match:
        sys.exit(f"Could not parse file_key from URL: {url}")
    file_key = match.group(1)

    node_match = re.search(r"node-id=([^&]+)", url)
    if not node_match:
        sys.exit(f"Could not parse node-id from URL: {url}")
    node_id = node_match.group(1)

    return file_key, node_id


def fetch_from_api(file_key: str, node_id: str, out: str) -> None:
    token = os.environ.get("FIGMA_ACCESS_TOKEN")
    if not token:
        sys.exit("FIGMA_ACCESS_TOKEN not set. Copy .env.example to .env and add your token.")

    print(f"Fetching Figma design for node {node_id} in file {file_key}...")

    api_url = f"https://api.figma.com/v1/images/{file_key}"
    api_node_id = node_id.replace("-", ":")
    params = {"ids": api_node_id, "format": "png", "scale": "2"}
    headers = {"X-Figma-Token": token}

    with httpx.Client(timeout=30) as client:
        resp = client.get(api_url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    if data.get("err"):
        sys.exit(f"Figma API error: {data['err']}")

    image_url = data.get("images", {}).get(node_id.replace("-", ":")) or next(
        iter(data.get("images", {}).values()), None
    )
    if not image_url:
        sys.exit(f"No image URL returned. Response: {data}")

    print("Downloading PNG from Figma CDN...")
    with httpx.Client(timeout=60) as client:
        img_resp = client.get(image_url)
        img_resp.raise_for_status()

    with open(out, "wb") as f:
        f.write(img_resp.content)

    print(f"Design saved to {out}")


def main():
    parser = argparse.ArgumentParser(description="Fetch a Figma frame as PNG")
    parser.add_argument("--url", required=True, help="Figma URL (must be a figma.com URL)")
    parser.add_argument("--out", required=True, help="Output path for PNG file")
    args = parser.parse_args()

    if "figma.com" not in args.url:
        sys.exit(f"Expected a Figma URL (figma.com), got: {args.url}")

    file_key, node_id = parse_figma_url(args.url)
    fetch_from_api(file_key, node_id, args.out)


if __name__ == "__main__":
    main()

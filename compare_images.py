import argparse

from PIL import Image, ImageDraw, ImageFont

LABEL_HEIGHT = 48
LABEL_BG = (30, 30, 30)
LABEL_FG = (255, 255, 255)
GAP = 8
GAP_COLOR = (200, 200, 200)


def load_font(size: int):
    for name in ["Arial.ttf", "Helvetica.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def side_by_side(left_path: str, right_path: str, out: str, left_label: str, right_label: str) -> None:
    left = Image.open(left_path).convert("RGB")
    right = Image.open(right_path).convert("RGB")

    # Scale both to the same height
    target_h = max(left.height, right.height)
    left = left.resize((int(left.width * target_h / left.height), target_h), Image.LANCZOS)
    right = right.resize((int(right.width * target_h / right.height), target_h), Image.LANCZOS)

    total_w = left.width + GAP + right.width
    canvas_h = LABEL_HEIGHT + target_h

    canvas = Image.new("RGB", (total_w, canvas_h), GAP_COLOR)

    # Label bar
    draw = ImageDraw.Draw(canvas)
    font = load_font(20)
    for x, w, text in [(0, left.width, left_label), (left.width + GAP, right.width, right_label)]:
        draw.rectangle([x, 0, x + w, LABEL_HEIGHT], fill=LABEL_BG)
        bbox = draw.textbbox((0, 0), text, font=font)
        tx = x + (w - (bbox[2] - bbox[0])) // 2
        ty = (LABEL_HEIGHT - (bbox[3] - bbox[1])) // 2
        draw.text((tx, ty), text, fill=LABEL_FG, font=font)

    canvas.paste(left, (0, LABEL_HEIGHT))
    canvas.paste(right, (left.width + GAP, LABEL_HEIGHT))

    canvas.save(out)
    print(f"Comparison saved to {out}  ({canvas.width}×{canvas.height})")


def main():
    parser = argparse.ArgumentParser(description="Stitch two screenshots side by side")
    parser.add_argument("--left", required=True, help="Left image path")
    parser.add_argument("--right", required=True, help="Right image path")
    parser.add_argument("--out", default="comparison.png", help="Output path")
    parser.add_argument("--left-label", default="Figma Design", help="Label for left image")
    parser.add_argument("--right-label", default="Live Page", help="Label for right image")
    args = parser.parse_args()

    side_by_side(args.left, args.right, args.out, args.left_label, args.right_label)


if __name__ == "__main__":
    main()

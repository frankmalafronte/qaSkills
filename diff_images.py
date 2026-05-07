import argparse

import numpy as np
from PIL import Image, ImageChops


def main():
    parser = argparse.ArgumentParser(description="Pixel diff between two images")
    parser.add_argument("--design", required=True, help="Design image path")
    parser.add_argument("--live", required=True, help="Live screenshot path")
    parser.add_argument("--out", default="/tmp/diff_amplified.png", help="Amplified diff output path")
    args = parser.parse_args()

    design = Image.open(args.design).convert("RGB")
    live = Image.open(args.live).convert("RGB")

    if design.size != live.size:
        print(f"Resizing live {live.size} → design {design.size}")
        live = live.resize(design.size, Image.LANCZOS)

    diff = ImageChops.difference(design, live)
    arr = np.array(diff)

    total_pixels = arr.shape[0] * arr.shape[1]
    nonzero = int(np.count_nonzero(arr.sum(axis=2)))
    mean_diff = float(arr.mean())
    max_diff = int(arr.max())

    amplified = Image.fromarray((arr * 10).clip(0, 255).astype(np.uint8))
    amplified.save(args.out)

    print(f"Design size:      {design.size}")
    print(f"Total pixels:     {total_pixels}")
    print(f"Differing pixels: {nonzero} ({nonzero / total_pixels * 100:.2f}%)")
    print(f"Mean diff:        {mean_diff:.4f}")
    print(f"Max channel diff: {max_diff}")
    print(f"Amplified diff:   {args.out}")


if __name__ == "__main__":
    main()

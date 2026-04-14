"""Data preparation utilities for training datasets."""

import argparse
from pathlib import Path

from PIL import Image


def resize_and_crop(
    image: Image.Image,
    resolution: int = 512,
    center_crop: bool = True,
) -> Image.Image:
    width, height = image.size

    if width < height:
        new_width = resolution
        new_height = int(height * (resolution / width))
    else:
        new_height = resolution
        new_width = int(width * (resolution / height))

    image = image.resize((new_width, new_height), Image.LANCZOS)

    if center_crop:
        left = (new_width - resolution) // 2
        top = (new_height - resolution) // 2
        image = image.crop((left, top, left + resolution, top + resolution))

    return image


def prepare_dataset(
    input_dir: str,
    output_dir: str,
    resolution: int = 512,
) -> int:
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    valid_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    processed = 0

    for image_file in sorted(input_path.iterdir()):
        if image_file.suffix.lower() not in valid_extensions:
            continue

        image = Image.open(image_file).convert("RGB")
        image = resize_and_crop(image, resolution)

        output_file = output_path / f"{image_file.stem}.png"
        image.save(output_file, "PNG")
        processed += 1

    print(f"Processed {processed} images → {output_path}")
    return processed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare training dataset")
    parser.add_argument("--input", type=str, required=True, help="Input image directory")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    parser.add_argument("--resolution", type=int, default=512, help="Target resolution")
    args = parser.parse_args()
    prepare_dataset(args.input, args.output, args.resolution)

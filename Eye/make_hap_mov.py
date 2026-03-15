#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory
import random
import subprocess
import sys

from PIL import Image


INPUT_GLOB = "eye-*.png"
OUTPUT_MOVIE = "Eye.mov"
FRAME_RATE = 1
OUTPUT_SIZE = (960, 540)

# Keep some margin inside the source image so slight zoom-out remains possible.
BASE_CROP_SCALE = 0.85
ZOOM_MIN = 0.95
ZOOM_MAX = 1.05

# Offset values are applied from the centered crop position.
BASE_OFFSET = (0, -48)
MAX_RANDOM_OFFSET = (24, 24)
MAX_RANDOM_ROTATION = 6.0

# Set to an integer for reproducible results.
RANDOM_SEED = None


def compute_base_crop(image_size):
    source_width, source_height = image_size
    output_width, output_height = OUTPUT_SIZE
    output_aspect = output_width / output_height

    max_crop_width = source_width
    max_crop_height = round(max_crop_width / output_aspect)

    if max_crop_height > source_height:
        max_crop_height = source_height
        max_crop_width = round(max_crop_height * output_aspect)

    base_crop_width = int(max_crop_width * BASE_CROP_SCALE)
    base_crop_height = round(base_crop_width / output_aspect)
    return base_crop_width, base_crop_height


def choose_crop_box(image_size, rng):
    source_width, source_height = image_size
    base_crop_width, base_crop_height = compute_base_crop(image_size)

    zoom = rng.uniform(ZOOM_MIN, ZOOM_MAX)
    crop_width = min(source_width, round(base_crop_width / zoom))
    crop_height = min(source_height, round(base_crop_height / zoom))

    max_x = source_width - crop_width
    max_y = source_height - crop_height
    center_x = max_x // 2
    center_y = max_y // 2

    base_offset_x, base_offset_y = BASE_OFFSET
    random_limit_x, random_limit_y = MAX_RANDOM_OFFSET
    offset_x = center_x + base_offset_x + rng.randint(-random_limit_x, random_limit_x)
    offset_y = center_y + base_offset_y + rng.randint(-random_limit_y, random_limit_y)
    offset_x = max(0, min(offset_x, max_x))
    offset_y = max(0, min(offset_y, max_y))

    return (
        offset_x,
        offset_y,
        offset_x + crop_width,
        offset_y + crop_height,
    )


def render_frame(image, rng):
    rotation = rng.uniform(-MAX_RANDOM_ROTATION, MAX_RANDOM_ROTATION)
    image = image.rotate(rotation, resample=Image.Resampling.BICUBIC)
    crop_box = choose_crop_box(image.size, rng)
    frame = image.crop(crop_box)
    return frame.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)


def render_frames(input_paths, temp_dir):
    rng = random.Random(RANDOM_SEED)

    with Image.open(input_paths[0]) as first_image:
        image_size = first_image.size

    for index, input_path in enumerate(input_paths):
        with Image.open(input_path) as image:
            image = image.convert("RGBA")
            frame = render_frame(image, rng)
            frame.save(temp_dir / f"frame-{index:03d}.png")

    return image_size


def encode_movie(temp_dir):
    command = [
        "ffmpeg",
        "-framerate",
        str(FRAME_RATE),
        "-i",
        str(temp_dir / "frame-%03d.png"),
        "-c:v",
        "hap",
        "-pix_fmt",
        "rgba",
        "-y",
        OUTPUT_MOVIE,
    ]
    subprocess.run(command, check=True)


def main():
    input_paths = sorted(Path(".").glob(INPUT_GLOB))

    if not input_paths:
        print(f"No input files matched {INPUT_GLOB}.", file=sys.stderr)
        return 1

    with TemporaryDirectory(prefix="hap_frames_", dir=".") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        image_size = render_frames(input_paths, temp_dir)
        encode_movie(temp_dir)

    print(
        f"Created {OUTPUT_MOVIE} from {len(input_paths)} frames "
        f"({image_size[0]}x{image_size[1]} -> {OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Entry program for the news-image-20261123 bounty.

Copies the pre-rendered broadsheet poster (entry.png, drawn with Pillow by
draw_poster.py in this repository) to the grader's output path and checks
that what it wrote is a whole 1024x1024 PNG under 1 MiB. Standard library
only, no network, no clock, no randomness: two runs write identical bytes
because they copy the same file.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
WANT_W, WANT_H = 1024, 1024


def png_size(path):
    """Read width/height straight out of a PNG's IHDR chunk."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR first")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    shutil.copyfile(SOURCE, target)

    size = os.path.getsize(target)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)
    width, height = png_size(target)
    if (width, height) != (WANT_W, WANT_H):
        raise SystemExit("entry.png is %dx%d, want 1024x1024" % (width, height))

    digest = hashlib.sha256()
    with open(target, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (target, size, width, height, digest.hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())

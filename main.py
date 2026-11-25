"""Jollof Under the Mango Tree entry.

Copies the baked invitation image (``entry.png``, shipped beside this file)
to ``entry.png`` in the output directory. The image is baked once at build
time; this program renders nothing.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUT", "/output")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "entry must be a PNG"
    assert head[12:16] == b"IHDR", "entry must carry an IHDR chunk"
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        path = os.path.join(OUT, name)
        if os.path.islink(path) or os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    size = os.path.getsize(SRC)
    assert size <= 1048576, "entry.png must be at most 1 MiB"
    width, height = png_size(SRC)
    assert (width, height) == (1024, 1024), "entry.png must be 1024x1024"
    shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
    dest = os.path.join(OUT, "entry.png")
    with open(SRC, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dest, "rb") as f:
        dest_hash = hashlib.sha256(f.read()).hexdigest()
    assert src_hash == dest_hash, "copied file must match the baked image"
    assert os.path.getsize(dest) <= 1048576, "copied file must be at most 1 MiB"
    assert png_size(dest) == (1024, 1024), "copied file must be 1024x1024"


if __name__ == "__main__":
    main()

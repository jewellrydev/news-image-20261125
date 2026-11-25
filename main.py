#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 25 November's world news in one image" bounty.

The repository holds the entry image as art.jpg (a JPEG, 1024x1024,
193,832 bytes — well under the 1 MiB limit). This program copies it,
byte for byte, to the output entry.png — the contest reads the image
format from the file's first bytes, so JPEG bytes in entry.png are
accepted. After copying it verifies the output's SHA-256 matches the
source, so a partial or failed write is never silently accepted.
Running it twice writes the same bytes both times.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "art.jpg")


def sha256_of(path: str) -> str:
    """SHA-256 of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    out_dir = os.environ.get("OUTPUT_DIR") or os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    source_hash = sha256_of(SOURCE)
    if sha256_of(dest) != source_hash:
        raise SystemExit("entry.png does not match art.jpg byte for byte")
    print(
        f"wrote entry.png from {os.path.basename(SOURCE)} "
        f"({os.path.getsize(dest)} bytes, sha256 {source_hash[:12]}…)"
    )


if __name__ == "__main__":
    main()

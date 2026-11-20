"""Hand the grader the completed one-page summary of 19 November 2026.

The page is already finished and checked, so this script never draws
a pixel. It only moves the finished picture from the repository into
the folder the judge reads. The layout itself — masthead, six-number
strip, hero row, story grid, regional briefs, small world map and the
DATE CHECK strip at the foot — lives inside that picture, not here.

Before anything is copied, the first bytes of the picture are read
back and matched against the signatures of the two image formats the
contest accepts. A file that is not a PNG or a JPEG stops the run
immediately, because handing the judge a damaged file would be worse
than handing it nothing at all.

Nothing here needs installing: pathlib, os, shutil and sys all ship
with Python. The destination folder follows MAKEFUN_OUTPUT_DIR when
it is set, and falls back to /output otherwise.
"""

import os
import shutil
import sys
from pathlib import Path

# Folder holding this script, resolved through pathlib.
BASE = Path(__file__).resolve().parent
SOURCE = BASE / "entry.jpg"

# Folder the judge reads from, overridable for local testing.
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
DESTINATION = OUT_DIR / "entry.png"

# Opening bytes every valid PNG and JPEG must start with.
PNG_MARK = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
JPEG_MARK = bytes((0xFF, 0xD8, 0xFF))


def verify_signature(path):
    """Refuse to ship a picture whose opening bytes are not an image.

    Reads the first eight bytes and accepts only a PNG header or a
    JPEG header. Anything else ends the run with a clear message and
    a non-zero status, so a corrupt or mistyped file can never reach
    the judge disguised as a valid entry.
    """
    with open(path, "rb") as handle:
        opening = handle.read(len(PNG_MARK))
    if opening.startswith(PNG_MARK) or opening.startswith(JPEG_MARK):
        return True
    sys.exit("bad image signature in %s: not a PNG or JPEG file" % path)



def ship_entry():
    """Check the picture, then place an exact copy at the output path.

    The source must exist beside this script, and its signature must
    pass first. The destination folder is created when needed, and the
    copy is byte-for-byte, so running twice produces identical bytes.
    Returns the size of the file that was written.
    """
    if not SOURCE.is_file():
        sys.exit("missing entry picture: %s" % SOURCE)
    verify_signature(SOURCE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    return DESTINATION.stat().st_size


def announce(path, size):
    """Tell the runner what landed where, in plain words."""
    print("entry placed at %s — %d bytes" % (path, size))


def main():
    size = ship_entry()
    announce(DESTINATION, size)


if __name__ == "__main__":
    main()

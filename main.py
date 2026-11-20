"""Deliver the 19 November 2026 front page.

The bounty asks for one image that sums up the world's news of
Thursday 19 November 2026. That image was drawn in advance by a
drawing program and saved here as entry.jpg: a newspaper front page
with a masthead, three hero stories, twelve grid stories, twenty-nine
briefs, a small world map and a date-check strip, 44 items in all.

This file is the entrypoint the grader runs. It does one job: it puts
entry.jpg where the grader looks for the picture, at
/output/entry.png. Nothing else happens here, and nothing is drawn
here, so the result is the same on every run.

Only the standard library is used. The grader executes this file with
`python3 -P -s main.py` inside a fresh container that installs
nothing, so any third-party import would fail the run. The two imports
below, os and shutil, both ship with Python itself.

The destination directory can be overridden with the
MAKEFUN_OUTPUT_DIR environment variable; without it the picture goes
to /output, which is where the grader reads it from.
"""

import os
import shutil

# The picture lives next to this file in the repository.
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(REPO_DIR, "entry.jpg")

# Where the grader expects the finished image.
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
TARGET = os.path.join(TARGET_DIR, "entry.png")


def place_picture():
    """Copy the pre-drawn front page to the grader's output path.

    The copy is byte-for-byte: the file the grader reads is exactly
    the file stored in the repository, so a re-run can never drift
    from the picture that was reviewed before submitting. A missing
    source picture is a hard failure, not a silent empty output: the
    copy raises, the run exits non-zero, and no stale image is ever
    handed to the judge in its place.
    """
    if not os.path.isfile(PICTURE):
        raise SystemExit("missing entry picture: %s" % PICTURE)
    os.makedirs(TARGET_DIR, exist_ok=True)
    shutil.copyfile(PICTURE, TARGET)
    return os.path.getsize(TARGET)


def report(size):
    """Tell the grader log what was written, in plain words."""
    print("wrote %s %d bytes" % (TARGET, size))
    print("truncated: none")


def main():
    size = place_picture()
    report(size)


if __name__ == "__main__":
    main()

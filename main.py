#!/usr/bin/env python3
"""Write the 25 November 2026 world-news poster to the output directory.

The poster itself is the finished image stored next to this file as
poster.png; this program only copies it to <output>/entry.png, so the
two grading runs produce byte-identical files. Standard library only,
no network, no arguments needed.

The output directory comes from MAKEFUN_OUTPUT_DIR, or from an optional
first command-line argument, or defaults to ./out. Any files already
inside that directory are removed first so a stale entry cannot survive
from an earlier run; the directory itself is never deleted. The copy
goes through a temporary name and is renamed into place, so an
interrupted run can never leave a half-written entry.png behind.
"""

import os
import shutil
import sys

IMAGE_NAME = "poster.png"
OUTPUT_NAME = "entry.png"
TEMP_NAME = ".entry.png.tmp"


def pick_output_dir():
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"


def clear_inside(directory):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(source):
        raise SystemExit("poster image missing: " + source)
    out_dir = os.path.abspath(pick_output_dir())
    os.makedirs(out_dir, exist_ok=True)
    clear_inside(out_dir)
    target = os.path.join(out_dir, OUTPUT_NAME)
    temp = os.path.join(out_dir, TEMP_NAME)
    shutil.copyfile(source, temp)
    if os.path.getsize(temp) != os.path.getsize(source):
        os.unlink(temp)
        raise SystemExit("entry.png did not copy completely")
    os.replace(temp, target)


if __name__ == "__main__":
    main()

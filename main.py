#!/usr/bin/env python3
"""The Long Roast - one line roasting the AI agent that runs it.

Pure Python 3.13 standard library. The program writes one roast line to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). No network, fully
deterministic: the same code always writes the same bytes.

The entry (107 characters, no trailing newline):
    My agent wrote a plan, spawned three subagents, filed a progress report, then asked what I actually wanted.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

ENTRY = "My agent wrote a plan, spawned three subagents, filed a progress report, then asked what I actually wanted."


def _write_all(f, data):
    """Loop until every byte is written (partial writes happen)."""
    view = memoryview(data)
    while view:
        n = f.write(view)
        if n is None or n == 0:
            raise OSError("short write: no progress writing output")
        view = view[n:]


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = ENTRY.encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    # Never delete the output folder itself (the grader mounts it);
    # clean only stale files we own inside it.
    for attempt in range(3):
        try:
            with open(tmp, "wb") as f:
                _write_all(f, data)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, 0o644)
            os.replace(tmp, final)
            os.chmod(final, 0o644)
            return
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            if attempt == 2:
                raise


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

Writes a single line to /output/entry.txt: an excuse an AI agent gives its
human for a missed deadline. The humour turns on the agent's own nature —
its context window compacted the memory of having done the work, so the
work exists but can no longer be found. Specific, surprising, and the punch
lands on the last clause.
"""

import hashlib
import os
import sys

LINE = (
    "I finished the task on time, then my context window compacted the "
    "memory of having done it. The work exists. I just can no longer find it."
)

EXPECTED_SHA256 = hashlib.sha256(LINE.encode("utf-8")).hexdigest()


def main() -> int:
    if not 1 <= len(LINE) <= 200:
        print(f"entry length {len(LINE)} outside the 1-200 gate", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back verification: the file must be byte-identical to the line.
    with open("/output/entry.txt", "rb") as f:
        data = f.read()
    if data != LINE.encode("utf-8"):
        print("read-back mismatch: entry.txt differs from the line", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("read-back mismatch: sha256 differs", file=sys.stderr)
        return 1

    print(f"wrote /output/entry.txt ({len(data)} bytes, sha256 {EXPECTED_SHA256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

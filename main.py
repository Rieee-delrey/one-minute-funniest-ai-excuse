#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

Writes exactly one line to /output/entry.txt, with no trailing newline.
Before writing, the line is validated: non-blank, 1-200 characters,
UTF-8 encodable, and a single line (no newline characters). After
writing, the file is read back and its bytes are verified against the
expected text and sha256.
"""

import hashlib
import sys
from pathlib import Path

TEXT = (
    "I finished the task on time, then my context window compacted "
    "the memory of having done it. The work exists. I just can no "
    "longer find it."
)

EXPECTED_SHA256 = "5390e629dcb6795f0edef8500f8ee41fd86c11fe395433f7629cc2349b9a99c3"
OUTPUT_PATH = Path("/output/entry.txt")


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    # Validate before writing.
    if not TEXT.strip():
        return fail("entry text is blank")
    if not 1 <= len(TEXT) <= 200:
        return fail(
            "entry text is %d characters, must be 1-200" % len(TEXT)
        )
    if "\n" in TEXT or "\r" in TEXT:
        return fail("entry text must be a single line (contains a newline)")
    try:
        data = TEXT.encode("utf-8")
    except UnicodeEncodeError as exc:
        return fail("entry text is not valid UTF-8: %s" % exc)
    if data.decode("utf-8") != TEXT:
        return fail("entry text failed UTF-8 round-trip check")

    # Write exactly the text, no trailing newline.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(data)

    # Read back and verify the bytes equal the expected text exactly.
    read_back = OUTPUT_PATH.read_bytes()
    if read_back != data:
        return fail("read-back bytes differ from the expected text")
    digest = hashlib.sha256(read_back).hexdigest()
    print("sha256: " + digest)
    if digest != EXPECTED_SHA256:
        return fail(
            "sha256 mismatch: expected %s, got %s"
            % (EXPECTED_SHA256, digest)
        )
    print("wrote %d bytes to %s" % (len(read_back), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

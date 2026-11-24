#!/usr/bin/env python3
"""Write the judged text artifact for the time-machine warning-label contest.

The judge scores only the exact bytes of /output/entry.txt. This program keeps
the line as a single constant, validates it against the published gate, and
publishes it with an atomic rename so a graded run can never see a partial
file.
"""

import hashlib
import os
import tempfile

ENTRY = (
    "WARNING: Do not travel to a time before this label was written. "
    "The label will be blank, and so will you."
)

MAX_CHARS = 120
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.txt"


def validated_bytes(text: str) -> bytes:
    """Apply the gate's checks explicitly; return the exact bytes to publish."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1 to {MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text.endswith("\n") or text.endswith("\r"):
        raise ValueError("entry must have no trailing newline")
    data = text.encode("utf-8")  # strict UTF-8; fails loudly on bad surrogates
    if data.decode("utf-8") != text:
        raise ValueError("entry is not a clean UTF-8 round-trip")
    return data


def main() -> None:
    data = validated_bytes(ENTRY)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    destination = os.path.join(OUTPUT_DIR, OUTPUT_NAME)

    # Atomic publish: same-directory temp file, fsync, rename over the target.
    fd, temp_path = tempfile.mkstemp(
        dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        dir_fd = os.open(OUTPUT_DIR, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

    # Clear verification output; the file itself stays exactly the judged line.
    print(f"artifact: {destination}")
    print(f"chars: {len(ENTRY)} / {MAX_CHARS}")
    print(f"bytes: {len(data)}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(f"entry: {ENTRY}")


if __name__ == "__main__":
    main()

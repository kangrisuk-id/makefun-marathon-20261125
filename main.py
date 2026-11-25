#!/usr/bin/env python3
"""One-Liner Marathon — entry program.

Writes the single winning one-liner to ``entry.txt`` in the output
directory the grader points us at. The joke was picked from a pool of
42 candidates in a scored head-to-head tournament against the judge's
published criteria (see candidates.md).

Pure standard library only: the grading image ships no third-party
packages, and this program needs none.
"""

import os
import sys

# The winning line. One line, 109 characters, well inside the gate's
# 1..280 character window. Do not add a trailing newline: the gate
# counts characters, and the text is judged exactly as written.
JOKE = (
    "The meeting could have been an email. "
    "The email could have been a shrug. "
    "The shrug is scheduled for Thursday."
)


def output_candidates():
    """Yield output directories in the order they should be tried."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield env_dir
    yield "/output"
    yield os.path.join(os.getcwd(), "output")


def write_entry(path: str) -> None:
    """Write the joke to *path*, then read it back and check the gate.

    The gate accepts UTF-8 text of 1 to 280 characters that is not only
    whitespace. Verifying our own output here means a bad write fails
    loudly in the run log instead of silently producing an invalid
    entry.
    """
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(JOKE)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != JOKE:
        raise OSError(f"read-back mismatch in {path}")
    if not (1 <= len(written) <= 280) or not written.strip():
        raise OSError(f"entry would fail the gate: {len(written)} chars")


def main() -> int:
    errors = []
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            write_entry(os.path.join(directory, "entry.txt"))
            return 0
        except OSError as exc:  # read-only or missing dir: try the next one
            errors.append(f"{directory}: {exc}")
    for line in errors:
        print(line, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

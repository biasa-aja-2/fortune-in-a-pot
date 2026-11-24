#!/usr/bin/env python3
"""Fortune in a Pot — one kind, funny fortune for a houseplant.

Writes a single fortune line to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``.

The fortune is written as if told to the plant sitting in its pot on the
windowsill: its roots are about to outgrow the pot, and its keeper is
finally going to upgrade it — a small, warm prediction, not a care
instruction and not a slogan.

Pure Python standard library only; no network, no randomness, no input
files. The output is fully deterministic.
"""

import os
import sys

# The fortune, exactly as it will be judged. One line, 111 characters,
# comfortably inside the competition's 120-character gate.
FORTUNE = (
    "Your roots will outgrow this pot by spring, and your human "
    "will buy you a bigger one for this sunny windowsill."
)

MAX_CHARS = 120


def check_fortune(text):
    """Return a list of gate failures; empty means the line is valid."""
    failures = []
    if not text:
        failures.append("fortune is empty")
    if text.strip() != text:
        failures.append("fortune has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        failures.append("fortune must be a single line")
    if len(text) > MAX_CHARS:
        failures.append(
            "fortune is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    if not text.strip():
        failures.append("fortune is only whitespace")
    for pos, ch in enumerate(text):
        code = ord(ch)
        if code < 0x20 and ch not in ("\t",):
            failures.append("control character U+%04X at position %d" % (code, pos))
        if code == 0x7F:
            failures.append("DEL character at position %d" % pos)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("not valid UTF-8: %s" % exc)
    return failures


def main():
    failures = check_fortune(FORTUNE)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(FORTUNE)

    # Read back and verify what actually landed on disk.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != FORTUNE:
        print("verification failed: entry.txt differs from fortune", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(written), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

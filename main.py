"""The Moon Gets One Star — a one-star review of the Moon.

Writes the review to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Deterministic: the same 111-character line on every run, no trailing
newline, single line, valid UTF-8.
"""

import os

REVIEW = (
    "One star. Open 14 nights a month, closed the rest with no notice, "
    "tides still wrong. Worst landlord in the sky."
)

MAX_CHARS = 120
MIN_CHARS = 1
OUTPUT_FILENAME = "entry.txt"


def validate(text):
    """Check the review meets the gate: 1-120 chars, single line, UTF-8.

    Returns the text unchanged when it passes; raises ValueError otherwise.
    """
    if not isinstance(text, str):
        raise ValueError("review must be a string")
    if len(text) < MIN_CHARS or text != text.strip():
        raise ValueError(
            "review must be non-blank with no leading/trailing whitespace"
        )
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"review is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    encoded = text.encode("utf-8")  # raises if not valid UTF-8
    if len(encoded) != len(text):
        # Non-ASCII characters are allowed, but keep the byte budget in view:
        # the gate counts characters, so only the character count binds us.
        pass
    return text


def write_entry(line, out_dir):
    """Write the validated line to entry.txt, then verify what landed."""
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise ValueError("entry.txt content does not match the review")
    return out_path


def main():
    line = validate(REVIEW)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(line, out_dir)


if __name__ == "__main__":
    main()

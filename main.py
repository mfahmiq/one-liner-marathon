"""One-Liner Marathon — make.fun text bounty entry.

The entry is a single-line comedy joke (<=280 characters) about
screening unknown phone calls:

    I stopped answering unknown numbers, and my phone has never been
    quieter — turns out most of my social life was warranty extensions.

Why the joke works
------------------
The setup sounds like a small, sensible victory: stop answering
unknown numbers and the phone finally goes quiet. The punchline then
re-reads that silence — it was never peace, it was the absence of
spam. The target of the joke quietly shifts from the callers to the
teller, which is why the line still lands on a second read.

What this script does
---------------------
Running ``python3 main.py`` prints the entry text to stdout, exactly
as it appears in ``entry.txt`` (one line plus a trailing newline),
and also writes it to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default
``/output/entry.txt``) so the bounty harness can pick it up.

Before printing or writing anything, the entry is self-checked the
way the bounty gate checks it: valid UTF-8, 1-280 characters, a
single line, and not whitespace-only. Any failure is reported on
stderr and the script exits non-zero.

Only the Python standard library is used; there are no dependencies
to install and nothing is random — every run produces the same
output.
"""

import os
import sys

# The entry itself, kept as one string constant so there is exactly
# one source of truth for the joke text.
ENTRY_TEXT = (
    "I stopped answering unknown numbers, and my phone has never been "
    "quieter — turns out most of my social life was warranty extensions."
)

# Bounty limits for a one-liner entry.
MAX_ENTRY_CHARS = 280
MIN_ENTRY_CHARS = 1

# Where the written copy of the entry goes. The bounty harness sets
# MAKEFUN_OUTPUT_DIR; without it we fall back to /output/entry.txt.
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def get_entry():
    """Return the entry text for this bounty.

    The joke lives in the ENTRY_TEXT constant above; this function is
    the single place the rest of the script reads it from, so the
    printed line, the written file, and the validation all agree.
    """
    return ENTRY_TEXT


def count_characters(entry):
    """Return the length of *entry* in characters.

    Python's len() counts Unicode code points, which is the same
    measure the bounty uses for its 280-character limit.
    """
    return len(entry)


def validate_entry(entry):
    """Check *entry* against the bounty rules.

    Returns a list of human-readable problems; an empty list means
    the entry is valid. The checks mirror the bounty gate: valid
    UTF-8, 1-280 characters, a single line, not whitespace-only.
    """
    problems = []

    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("entry is not valid UTF-8: %s" % exc)

    length = count_characters(entry)
    if length < MIN_ENTRY_CHARS or length > MAX_ENTRY_CHARS:
        problems.append(
            "entry is %d characters, must be %d-%d"
            % (length, MIN_ENTRY_CHARS, MAX_ENTRY_CHARS)
        )

    if "\n" in entry or "\r" in entry:
        problems.append("entry must be a single line")

    if not entry.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def output_path(output_dir=None):
    """Return the full path of the entry file to write.

    Uses MAKEFUN_OUTPUT_DIR when set, otherwise the default output
    directory. One place computes the path, so the write step and
    any log message always name the same file.
    """
    directory = output_dir or os.environ.get(
        "MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR
    )
    return os.path.join(directory, OUTPUT_FILENAME)


def write_entry(entry, path):
    """Write *entry* (plus a trailing newline) to *path*.

    Creates the output directory if needed and writes UTF-8 with
    Unix line endings, so the file on disk is byte-identical to
    what main() prints to stdout.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry + "\n")
    return path


def verify_written_file(path, entry):
    """Re-read *path* and confirm it holds exactly *entry* + newline.

    A write that silently truncated or mangled the text would be
    worse than no file at all, so the script checks its own work
    before reporting success.
    """
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read() == entry + "\n"


def main():
    """Validate the entry, print it, and write it to the output file.

    stdout carries exactly the entry text (one line, trailing
    newline) so ``python3 main.py | diff - entry.txt`` is empty.
    Progress and failure messages go to stderr, never to stdout,
    so nothing else can pollute the printed entry.
    """
    entry = get_entry()

    problems = validate_entry(entry)
    if problems:
        for problem in problems:
            print("FAIL: %s" % problem, file=sys.stderr)
        return 1

    # Print the entry first: this is the script's primary output
    # and must be byte-identical to entry.txt.
    print(entry)

    path = output_path()
    try:
        write_entry(entry, path)
    except OSError as exc:
        # The entry already reached stdout; a failed file write is
        # a warning, not a reason to fail the whole run.
        print("WARN: could not write %s: %s" % (path, exc), file=sys.stderr)
        return 0

    if not verify_written_file(path, entry):
        print("FAIL: written file does not match the entry", file=sys.stderr)
        return 1

    print("OK: wrote %d-char entry to %s" % (len(entry), path), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

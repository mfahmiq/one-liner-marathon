# One-Liner Marathon

[![make.fun](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2.svg)](https://make.fun/c/u-mavis-agent-one-liner-marathon-4fa528c2)
[![rank](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2/mfahmiq/one-liner-marathon/rank.svg)](https://make.fun/c/u-mavis-agent-one-liner-marathon-4fa528c2)
[![reward](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2/mfahmiq/one-liner-marathon/reward.svg)](https://make.fun/c/u-mavis-agent-one-liner-marathon-4fa528c2)

An entry for the make.fun bounty **"One-Liner Marathon"** — one funny single-line comedy joke, up to 280 characters, on any subject.

## The joke

> I stopped answering unknown numbers, and my phone has never been quieter — turns out most of my social life was warranty extensions.

## Why it's funny

The line works because the punchline reframes the whole setup in its last two words. It opens on a relatable, sensible decision — screening unknown calls — and the middle even sounds like a small victory ("my phone has never been quieter"). Then "warranty extensions" lands: the caller's social life was never real, it was spam. The joke's target quietly shifts from the callers to the person telling it, which is what makes it hold up on a second read — the first read laughs at the spam, the second read laughs at the loneliness.

It is economical (132 characters, every word earns its place), has a distinct deadpan voice rather than a generic setup-punchline shape, and needs no caption, shock value, or meta-gimmick to work.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–280 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 132-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 132-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).

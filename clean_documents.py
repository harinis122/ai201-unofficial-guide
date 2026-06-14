"""
Stage 2 of the pipeline (see planning.md "Architecture"): cleaning.

Reads the raw, uncleaned source files in documents/ and writes a cleaned copy of
each to cleaned_documents/ using the same filename. Raw files are never modified.

What gets removed:
  - Reddit: nav chrome (Go to UCI, r/UCI, the • / · separators), usernames and
    "u/... avatar" lines, relative timestamps ("4y ago"), vote counts, MOD/OP
    badges, "Comments Section", "[deleted]"/"[removed]", "N more replies", and
    whole "Promoted" ad blocks (ad copy + CTA + domain + image caption). Share
    tracking (?utm_source=share...) is stripped from any links that are kept.
  - Transcripts (YouTube tour + official webinar): timestamps in both forms
    (inline "1:081 minute, 8 seconds..." and standalone "48:07" lines) and
    [Music]/[Applause] markers. Wrapped lines are rejoined into flowing prose.

What is kept: the actual post bodies, comments, opinions, descriptions, and the
transcript speech. Chapter headings in the tour ("Chapter 3: Plaza Verde (PV)")
are kept because they say which complex is being described.

Chunking is intentionally NOT done here -- that is the next pipeline stage.
"""

import re
from pathlib import Path

RAW_DIR = Path(__file__).parent / "documents"
CLEAN_DIR = Path(__file__).parent / "cleaned_documents"

# Map each raw filename to the cleaner it needs. Anything not listed here is
# treated as a Reddit thread (the 8 reddit sources).
TRANSCRIPT_YOUTUBE = "uci_housing.txt"
TRANSCRIPT_OFFICIAL = "uci_official_housing.txt"


# --------------------------------------------------------------------------- #
# Reddit cleaning
# --------------------------------------------------------------------------- #

# Lines that are pure boilerplate and should be dropped entirely.
_REDDIT_EXACT_DROP = {
    "go to uci",
    "comments section",
    "mod",
    "op",
    "promoted",
    "learn more",
    "shop now",
    "sign up",
    "collapse video player",
    "collapse",
    "continue this thread",
    "[deleted]",
    "[removed]",
    "0:00 / 0:00",
    "•",
    "·",
}

# Relative timestamps like "4y ago", "13y ago", "5 months ago".
_RE_RELATIVE_TIME = re.compile(
    r"^\d+\s*"
    r"(?:s|sec|secs|second|seconds|m|min|mins|minute|minutes|h|hr|hrs|hour|hours"
    r"|d|day|days|w|wk|wks|week|weeks|mo|mos|month|months|y|yr|yrs|year|years)"
    r"\s+ago$",
    re.IGNORECASE,
)
_RE_AVATAR = re.compile(r"^u/\S+\s+avatar$", re.IGNORECASE)
_RE_USERNAME_HANDLE = re.compile(r"^u/[\w-]+$", re.IGNORECASE)
# A bare one-word line with no spaces: in this export that is always a username
# (real comment/post text is full sentences with spaces).
_RE_BARE_TOKEN = re.compile(r"^[A-Za-z0-9_-]{2,30}$")
_RE_VOTE_COUNT = re.compile(r"^-?\d{1,7}$")
_RE_MORE_REPLIES = re.compile(r"^\d+\s+more\s+repl(?:y|ies)$", re.IGNORECASE)
_RE_DOMAIN_ONLY = re.compile(r"^[\w-]+(?:\.[\w-]+)+$")  # e.g. uber.com, disneyplus.com
_RE_IMG_CAPTION = re.compile(r"^(?:thumbnail image:|clickable image)", re.IGNORECASE)
# Share tracking appended to links: ?utm_source=share&utm_medium=...&context=3
_RE_UTM = re.compile(r"[?&]utm_source=share[^\s]*")


def _excise_promoted_ads(lines):
    """Remove whole 'Promoted' ad blocks.

    An ad runs from the 'u/<advertiser> avatar' line that precedes 'Promoted'
    through the ad's image-caption line ('Thumbnail image:' / 'Clickable
    image...'), which is the last line of the ad unit. Trailing markers like
    'Collapse video player' and '0:00 / 0:00' are caught by the line filter.
    """
    while True:
        promoted_idx = next(
            (i for i, ln in enumerate(lines) if ln.strip().lower() == "promoted"),
            None,
        )
        if promoted_idx is None:
            return lines

        # Walk back to the avatar line that opens the ad unit.
        start = promoted_idx
        for i in range(promoted_idx - 1, max(promoted_idx - 5, -1), -1):
            if _RE_AVATAR.match(lines[i].strip()):
                start = i
                break
        else:
            start = max(promoted_idx - 1, 0)

        # Walk forward to the image caption that closes the ad unit.
        end = promoted_idx
        for i in range(promoted_idx + 1, min(promoted_idx + 8, len(lines))):
            if _RE_IMG_CAPTION.match(lines[i].strip()):
                end = i
                break
        else:
            # No caption found: fall back to dropping just through the domain
            # line so we never run away and eat real comments.
            end = promoted_idx
            for i in range(promoted_idx + 1, min(promoted_idx + 6, len(lines))):
                if _RE_DOMAIN_ONLY.match(lines[i].strip()):
                    end = i
                    break

        del lines[start : end + 1]


def _is_reddit_boilerplate(line):
    s = line.strip()
    if not s:
        return False  # keep blanks for now; collapsed later
    low = s.lower()
    if low in _REDDIT_EXACT_DROP:
        return True
    if low.startswith("r/") and " " not in s:
        return True
    return bool(
        _RE_RELATIVE_TIME.match(s)
        or _RE_AVATAR.match(s)
        or _RE_USERNAME_HANDLE.match(s)
        or _RE_VOTE_COUNT.match(s)
        or _RE_MORE_REPLIES.match(s)
        or _RE_DOMAIN_ONLY.match(s)
        or _RE_IMG_CAPTION.match(s)
        or _RE_BARE_TOKEN.match(s)
    )


def clean_reddit_text(raw):
    lines = raw.splitlines()
    lines = _excise_promoted_ads(lines)

    kept = []
    for line in lines:
        if _is_reddit_boilerplate(line):
            continue
        line = _RE_UTM.sub("", line)  # strip share tracking from kept links
        kept.append(line.rstrip())

    return _collapse_blank_lines("\n".join(kept))


# --------------------------------------------------------------------------- #
# Transcript cleaning (YouTube tour + official webinar)
# --------------------------------------------------------------------------- #

_RE_CHAPTER = re.compile(r"^Chapter\s+\d+\s*:", re.IGNORECASE)
# Standalone timestamp on its own line: "48:07", "1:23:04".
_RE_TS_STANDALONE = re.compile(r"^\d{1,2}(?::\d{2}){1,2}$")
# Inline timestamp + YouTube's verbose duration glued to the start of the text:
# "0:011 second...", "1:081 minute, 8 seconds...", "1:23:0445 minutes...".
_RE_TS_INLINE = re.compile(
    r"^\d{1,2}(?::\d{2}){1,2}"
    r"(?:\s*\d+\s+(?:hours?|minutes?|seconds?)(?:,\s*)?)+"
)
_RE_BRACKET_MARKER = re.compile(r"\[(?:music|applause|laughter|inaudible)\]", re.IGNORECASE)


def _strip_timestamps(line):
    """Remove a leading timestamp (either form) and bracket markers from a line."""
    s = _RE_TS_INLINE.sub("", line)
    s = _RE_BRACKET_MARKER.sub(" ", s)
    return s.strip()


def clean_transcript_text(raw):
    """Clean the YouTube housing-tour transcript, preserving chapter headings."""
    sections = []  # list of [header_or_None, [text fragments]]
    current = [None, []]
    sections.append(current)

    for line in raw.splitlines():
        s = line.strip()
        if not s or _RE_TS_STANDALONE.match(s):
            continue
        if _RE_CHAPTER.match(s):
            current = [s, []]
            sections.append(current)
            continue
        text = _strip_timestamps(s)
        if text:
            current[1].append(text)

    blocks = []
    for header, frags in sections:
        body = re.sub(r"\s+", " ", " ".join(frags)).strip()
        if header and body:
            blocks.append(f"{header}\n{body}")
        elif header:
            blocks.append(header)
        elif body:
            blocks.append(body)
    return "\n\n".join(blocks)


def clean_official_page_text(raw):
    """Clean the official webinar transcript into flowing prose (no chapters)."""
    fragments = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or _RE_TS_STANDALONE.match(s):
            continue
        text = _strip_timestamps(s)
        if text:
            fragments.append(text)
    return re.sub(r"\s+", " ", " ".join(fragments)).strip()


# --------------------------------------------------------------------------- #
# Shared helpers + driver
# --------------------------------------------------------------------------- #

def _collapse_blank_lines(text):
    text = re.sub(r"[ \t]+\n", "\n", text)        # trailing whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)         # 3+ blank lines -> one
    return text.strip() + "\n"


def clean_file(path):
    raw = path.read_text(encoding="utf-8")
    if path.name == TRANSCRIPT_YOUTUBE:
        cleaned = clean_transcript_text(raw)
    elif path.name == TRANSCRIPT_OFFICIAL:
        cleaned = clean_official_page_text(raw)
    else:
        cleaned = clean_reddit_text(raw)
    return raw, cleaned.strip() + "\n"


def main():
    CLEAN_DIR.mkdir(exist_ok=True)
    raw_files = sorted(p for p in RAW_DIR.glob("*.txt"))
    if not raw_files:
        print(f"No .txt files found in {RAW_DIR}")
        return

    print(f"Cleaning {len(raw_files)} documents -> {CLEAN_DIR}/\n")
    print(f"{'file':<40}{'raw':>8}{'clean':>8}{'kept':>7}")
    print("-" * 63)
    for path in raw_files:
        raw, cleaned = clean_file(path)
        out = CLEAN_DIR / path.name
        out.write_text(cleaned, encoding="utf-8")
        pct = (len(cleaned) / len(raw) * 100) if raw else 0
        print(f"{path.name:<40}{len(raw):>8}{len(cleaned):>8}{pct:>6.0f}%")


if __name__ == "__main__":
    main()

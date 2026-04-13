"""Validate a protocol README against template requirements and optional source text."""

from pathlib import Path
import re
import sys
from typing import List, Optional, Tuple

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(
    r"^### Status:\s+.*`\[(?:OK|\?|X)\]`.*$",
    re.MULTILINE,
)
STATUS_LEGEND_RE = re.compile(
    r"^\| \*\*\*Status legend\*\*\*:.*`\[OK\]`.*`\[\?\]`.*`\[X\]`.*\|$",
    re.MULTILINE,
)
PLACEHOLDER_STEP_HEADING_RE = re.compile(
    r"^#{1,6}\s+\d+(?:\.\d+)*(?:\.)?\s+(?:Step|Sub-step)\b.*$",
    re.MULTILINE,
)
PLACEHOLDER_CONTENTS_RE = re.compile(
    r"^\d+\.\s+\[Step\s+\d+\]\(#.*$",
    re.MULTILINE,
)

REQUIRED_HEADINGS = [
    (1, "About"),
    (2, "Contents"),
]

BAD_PLACEHOLDERS = {
    "TODO": re.compile(r"\bTODO\b"),
    "TBD": re.compile(r"\bTBD\b"),
    "XXX": re.compile(r"\bXXX\b"),
    "CHECK:": re.compile(r"CHECK:"),
}

DISALLOWED_TEMPLATE_TEXT = [
    "Template repository: Click `Use this template` to create a new protocol repo.",
]


def extract_headings(text: str) -> List[Tuple[int, str]]:
    return [(len(level), title.strip()) for level, title in HEADING_RE.findall(text)]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("µ", "u"))


def canonicalize_measurement(token: str) -> str:
    token = normalize_text(token)
    token = token.replace("°", "")
    token = re.sub(r"\s+", "", token)

    time_match = re.fullmatch(r"(\d+(?:\.\d+)?)(seconds|second|secs|sec|s|minutes|minute|mins|min|hours|hour|hrs|hr)", token)
    if time_match:
        value, unit = time_match.groups()
        unit_map = {
            "seconds": "s",
            "second": "s",
            "secs": "s",
            "sec": "s",
            "s": "s",
            "minutes": "min",
            "minute": "min",
            "mins": "min",
            "min": "min",
            "hours": "h",
            "hour": "h",
            "hrs": "h",
            "hr": "h",
        }
        return f"{value}{unit_map[unit]}"

    temp_match = re.fullmatch(r"(\d+(?:\.\d+)?)(c)", token)
    if temp_match:
        value, unit = temp_match.groups()
        return f"{value}{unit}"

    volume_or_mass_match = re.fullmatch(r"(\d+(?:\.\d+)?)(ul|ml|l|g|mg|kg|ng|ug)", token)
    if volume_or_mass_match:
        value, unit = volume_or_mass_match.groups()
        return f"{value}{unit}"

    percent_match = re.fullmatch(r"(\d+(?:\.\d+)?)%", token)
    if percent_match:
        return token

    return token


def extract_key_tokens(text: str) -> List[str]:
    patterns = [
        r"\b\d+(?:\.\d+)?\s*(?:µL|uL|mL|L|g|mg|kg|ng|µg)\b",
        r"\b\d+(?:\.\d+)?\s*(?:seconds|second|minutes|minute|hours|hour|s|sec|secs|min|mins|hr|hrs)\b",
        r"\b\d+(?:\.\d+)?\s*°?\s*C\b",
        r"\b\d+(?:\.\d+)?%\b",
    ]
    hits = []
    for pattern in patterns:
        hits.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return sorted(set(hits))


def validate_readme(readme: str, source: Optional[str] = None) -> List[str]:
    failures: List[str] = []
    headings = extract_headings(readme)
    top_level_headings = [title for level, title in headings if level == 1]

    if not headings:
        failures.append("README does not contain any Markdown headings.")
    elif not top_level_headings:
        failures.append("README must contain a top-level protocol title ('# ...').")
    else:
        first_title = top_level_headings[0]
        if first_title == "About":
            failures.append("Missing top-level protocol title before '# About'.")

    for level, title in REQUIRED_HEADINGS:
        if (level, title) not in headings:
            failures.append(f"Missing heading: {'#' * level} {title}")

    if not STATUS_LINE_RE.search(readme):
        failures.append("Missing or malformed status line: expected '### Status: ...'.")

    if not STATUS_LEGEND_RE.search(readme):
        failures.append(
            "Missing or malformed status legend row with `[OK]`, `[?]`, and `[X]`."
        )

    for token, pattern in BAD_PLACEHOLDERS.items():
        if pattern.search(readme):
            failures.append(f"Found unresolved placeholder: {token}")

    for text in DISALLOWED_TEMPLATE_TEXT:
        if text in readme:
            failures.append(f"Found template-only text that must be removed: {text}")

    for match in PLACEHOLDER_STEP_HEADING_RE.findall(readme):
        failures.append(f"Found placeholder step heading: {match}")

    for match in PLACEHOLDER_CONTENTS_RE.findall(readme):
        failures.append(f"Found placeholder contents entry: {match}")

    if source is not None:
        readme_tokens = {
            canonicalize_measurement(token) for token in extract_key_tokens(readme)
        }
        for token in extract_key_tokens(source):
            if canonicalize_measurement(token) not in readme_tokens:
                failures.append(f"Source token missing from README: {token}")

    return list(dict.fromkeys(failures))


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        print("Usage: python validate_protocol.py README.md [legacy/source.txt]")
        sys.exit(1)

    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    source = Path(sys.argv[2]).read_text(encoding="utf-8") if len(sys.argv) == 3 else None

    failures = validate_readme(readme, source)

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()

"""Validate a protocol README against required template elements and source text."""

from pathlib import Path
import re
import sys

REQUIRED_HEADINGS = [
    "# About",
    "### Status:",
    "## Contents",
    "***Status legend***:"
]

BAD_PLACEHOLDERS = [
    "TODO",
    "TBD",
    "XXX",
    "CHECK:",
]

def extract_key_tokens(text: str):
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_protocol.py README.md legacy/source.txt")
        sys.exit(1)

    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    source = Path(sys.argv[2]).read_text(encoding="utf-8")

    failures = []

    for heading in REQUIRED_HEADINGS:
        if heading not in readme:
            failures.append(f"Missing heading: {heading}")

    for token in BAD_PLACEHOLDERS:
        if token in readme:
            failures.append(f"Found unresolved placeholder: {token}")

    source_tokens = extract_key_tokens(source)
    for token in source_tokens:
        if token not in readme:
            if token.lower() not in readme.lower():
                failures.append(f"Source token missing from README: {token}")

    # if "## Unplaced content" not in readme:
    #     failures.append("Missing '## Unplaced content' section")

    # if "## CHECK items" not in readme:
    #     failures.append("Missing '## CHECK items' section")

    if failures:
        print("VALIDATION FAILED")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)

    print("Validation passed.")

if __name__ == "__main__":
    main()

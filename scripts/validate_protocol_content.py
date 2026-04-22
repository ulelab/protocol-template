"""Validate protocol README content against template requirements."""

from pathlib import Path
import re
import sys
from typing import List, Tuple

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
    (1, "Materials"),
]

BAD_PLACEHOLDERS = {
    "TODO": re.compile(r"\bTODO\b"),
    "TBD": re.compile(r"\bTBD\b"),
    "XXX": re.compile(r"\bXXX\b"),
    "CHECK:": re.compile(r"CHECK:"),
}

DISALLOWED_TEMPLATE_TEXT = [
    "> Template repository: Click `Use this template` to create a new protocol repo. Template docs are in [docs/USING_THIS_TEMPLATE.md](https://github.com/ulelab/protocol-template/blob/main/docs/USING_THIS_TEMPLATE.md)",
]


def extract_headings(text: str) -> List[Tuple[int, str]]:
    return [(len(level), title.strip()) for level, title in HEADING_RE.findall(text)]


def normalize_heading_title(title: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*(?:\.)?\s+", "", title).strip()


def has_required_heading(
    headings: List[Tuple[int, str]],
    required_level: int,
    required_title: str,
) -> bool:
    return any(
        level == required_level and normalize_heading_title(title) == required_title
        for level, title in headings
    )


def validate_readme(readme: str) -> List[str]:
    failures: List[str] = []
    headings = extract_headings(readme)
    top_level_headings = [title for level, title in headings if level == 1]

    if not headings:
        failures.append("README does not contain any Markdown headings.")
    elif not top_level_headings:
        failures.append("README must contain a top-level protocol title ('# ...').")
    else:
        first_title = normalize_heading_title(top_level_headings[0])
        if first_title == "About":
            failures.append("Missing top-level protocol title before '# About'.")

    for level, title in REQUIRED_HEADINGS:
        if not has_required_heading(headings, level, title):
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

    return list(dict.fromkeys(failures))


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python validate_protocol_content.py README.md")
        sys.exit(1)

    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    failures = validate_readme(readme)

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Content validation passed.")


if __name__ == "__main__":
    main()

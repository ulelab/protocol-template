"""Backward-compatible entrypoint for protocol README validation."""

from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple

try:
    from scripts.validate_protocol_content import validate_readme as validate_content
    from scripts.validate_protocol_style import validate_readme_style
except ModuleNotFoundError:
    from validate_protocol_content import validate_readme as validate_content
    from validate_protocol_style import validate_readme_style


def extract_headings(text: str) -> List[Tuple[int, str]]:
    return [(len(level), title.strip()) for level, title in HEADING_RE.findall(text)]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("µ", "u").replace("μ", "u"))


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def canonicalize_measurement(token: str) -> str:
    token = normalize_text(token)
    token = token.replace("°", "")
    token = token.replace(",", "")
    token = re.sub(r"\bx\s*", "", token)
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

    volume_or_mass_match = re.fullmatch(
        r"(\d+(?:\.\d+)?)(ul|ml|l|g|mg|kg|ng|ug)", token
    )
    if volume_or_mass_match:
        value, unit = volume_or_mass_match.groups()
        return f"{value}{unit}"

    percent_match = re.fullmatch(r"(\d+(?:\.\d+)?)%", token)
    if percent_match:
        return token

    return token


def extract_key_token_occurrences(text: str) -> List[Tuple[str, int]]:
    patterns = [
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:[µμu]L|mL|L|mg|kg|ng|[µμu]g)\b",
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:x\s*)?g\b",
        r"\b\d+(?:\.\d+)?\s*(?:seconds|second|minutes|minute|hours|hour|s|sec|secs|min|mins|hr|hrs)\b",
        r"\b\d+(?:\.\d+)?\s*°?\s*C\b",
        r"\b\d+(?:\.\d+)?%\b",
    ]
    hits: List[Tuple[str, int]] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            hits.append((match.group(0), line_number_for_offset(text, match.start())))
    return hits


def first_line_for_text(text: str, snippet: str) -> Optional[int]:
    index = text.find(snippet)
    if index == -1:
        return None
    return line_number_for_offset(text, index)


def first_line_for_regex(text: str, pattern: re.Pattern) -> Optional[int]:
    match = pattern.search(text)
    if match is None:
        return None
    return line_number_for_offset(text, match.start())


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
        line = first_line_for_regex(readme, pattern)
        if line is not None:
            failures.append(f"Found unresolved placeholder: {token} (README line {line})")

    for text in DISALLOWED_TEMPLATE_TEXT:
        if text in readme:
            line = first_line_for_text(readme, text)
            if line is None:
                failures.append(f"Found template-only text that must be removed: {text}")
            else:
                failures.append(
                    f"Found template-only text that must be removed: {text} (README line {line})"
                )

    for match in PLACEHOLDER_STEP_HEADING_RE.finditer(readme):
        line = line_number_for_offset(readme, match.start())
        failures.append(
            f"Found placeholder step heading: {match.group(0)} (README line {line})"
        )

    for match in PLACEHOLDER_CONTENTS_RE.finditer(readme):
        line = line_number_for_offset(readme, match.start())
        failures.append(
            f"Found placeholder contents entry: {match.group(0)} (README line {line})"
        )

    if source is not None:
        readme_tokens: Dict[str, List[Tuple[str, int]]] = {}
        for token, line in extract_key_token_occurrences(readme):
            readme_tokens.setdefault(canonicalize_measurement(token), []).append(
                (token, line)
            )

        source_tokens: Dict[str, List[Tuple[str, int]]] = {}
        for token, line in extract_key_token_occurrences(source):
            source_tokens.setdefault(canonicalize_measurement(token), []).append(
                (token, line)
            )

        for canonical_token, occurrences in source_tokens.items():
            if canonical_token in readme_tokens:
                continue

            raw_token, first_source_line = occurrences[0]
            all_source_lines = ", ".join(str(line) for _, line in occurrences)
            failures.append(
                "Source token missing from README: "
                f"{raw_token} (source line {first_source_line}; all source lines: {all_source_lines})"
            )

    return list(dict.fromkeys(failures))


def main() -> None:
    if len(sys.argv) not in {2, 3}:
        print("Usage: python validate_protocol.py README.md [legacy/source.txt]")
        sys.exit(1)

    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    failures = validate_readme(readme)

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()

"""Validate protocol README unit and notation style."""

from pathlib import Path
import re
import sys
from typing import List

NUMBER_RE = r"\d+(?:\.\d+)?"
TEMPERATURE_RE = re.compile(
    rf"\b(?P<value>{NUMBER_RE})(?P<space1>\s*)(?P<degree>°?)(?P<space2>\s*)(?P<unit>[Cc])\b"
)
PH_RE = re.compile(r"\b(?P<label>[Pp][Hh])(?P<space>\s*)(?P<value>\d+(?:\.\d+)?)\b")
MICRO_UNIT_RE = re.compile(
    rf"\b(?P<value>{NUMBER_RE})(?P<space>\s*)(?P<unit>uL|ul|UL|uM|UM|ug|μL|μM|μg)\b"
)
UNIT_RE = re.compile(
    rf"\b(?P<value>{NUMBER_RE})(?P<space>\s*)(?P<unit>µL|mL|ml|ML|L|l|µg|mg|g|kg|ng|mM|µM|nM|M|μL|μM|μg)\b"
)
TIME_RE = re.compile(
    rf"\b(?P<value>{NUMBER_RE})(?P<space>\s*)(?P<unit>seconds?|second|minutes?|minute|hours?|hour|secs?|sec|mins?|min|hrs?|hr|s|h)\b",
    re.IGNORECASE,
)

PREFERRED_MICRO_UNITS = {
    "ul": "µL",
    "um": "µM",
    "ug": "µg",
    "μl": "µL",
    "μm": "µM",
    "μg": "µg",
}
PREFERRED_UNITS = {
    "µl": "µL",
    "μl": "µL",
    "ml": "mL",
    "l": "L",
    "µg": "µg",
    "μg": "µg",
    "mg": "mg",
    "g": "g",
    "kg": "kg",
    "ng": "ng",
    "mm": "mM",
    "µm": "µM",
    "μm": "µM",
    "m": "M",
}
TIME_UNIT_BASE = {
    "s": "second",
    "sec": "second",
    "secs": "second",
    "second": "second",
    "seconds": "second",
    "min": "minute",
    "mins": "minute",
    "minute": "minute",
    "minutes": "minute",
    "h": "hour",
    "hr": "hour",
    "hrs": "hour",
    "hour": "hour",
    "hours": "hour",
}


def preferred_time_token(value: str, unit: str) -> str:
    base = TIME_UNIT_BASE[unit.lower()]
    plural = "" if value == "1" else "s"
    return f"{value} {base}{plural}"


def validate_readme_style(readme: str) -> List[str]:
    failures: List[str] = []

    for line_number, line in enumerate(readme.splitlines(), start=1):
        for match in TEMPERATURE_RE.finditer(line):
            preferred = f"{match.group('value')} °C"
            if match.group(0) != preferred:
                failures.append(
                    f"Line {line_number}: temperature should use `{preferred}` style, found `{match.group(0)}`."
                )

        for match in MICRO_UNIT_RE.finditer(line):
            preferred_unit = PREFERRED_MICRO_UNITS[match.group("unit").lower()]
            preferred = f"{match.group('value')} {preferred_unit}"
            if match.group(0) != preferred:
                failures.append(
                    f"Line {line_number}: unit should use `{preferred}` style, found `{match.group(0)}`."
                )

        for match in UNIT_RE.finditer(line):
            preferred_unit = PREFERRED_UNITS[match.group("unit").lower()]
            preferred = f"{match.group('value')} {preferred_unit}"
            if match.group(0) != preferred:
                failures.append(
                    f"Line {line_number}: unit should use `{preferred}` style, found `{match.group(0)}`."
                )

        for match in TIME_RE.finditer(line):
            preferred = preferred_time_token(match.group("value"), match.group("unit"))
            if match.group(0) != preferred:
                failures.append(
                    f"Line {line_number}: time should use full-word units like `{preferred}`, found `{match.group(0)}`."
                )

        for match in PH_RE.finditer(line):
            preferred = f"pH {match.group('value')}"
            if match.group(0) != preferred:
                failures.append(
                    f"Line {line_number}: pH should use `{preferred}` style, found `{match.group(0)}`."
                )

    return list(dict.fromkeys(failures))


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python validate_protocol_style.py README.md")
        sys.exit(1)

    readme = Path(sys.argv[1]).read_text(encoding="utf-8")
    failures = validate_readme_style(readme)

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Style validation passed.")


if __name__ == "__main__":
    main()

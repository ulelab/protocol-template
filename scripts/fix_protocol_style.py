"""Apply deterministic style fixes to a protocol README."""

from pathlib import Path
import argparse
import re
from typing import Callable, Match

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
CHEMICAL_FORMULA_RE = re.compile(r"\b(?P<formula>(?:[A-Z][a-z]?\d*){2,})\b")
UNICODE_SUBSCRIPT_RE = re.compile(r"\b(?P<formula>[A-Za-z₀₁₂₃₄₅₆₇₈₉]+)\b")

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
UNICODE_SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
NOTE_LABEL_RE = re.compile(
    r"^(?P<indent>\s*)(?P<label>Note|NOTE|NB|Optional|Recommended|Warning):\s*(?P<body>.*)$",
    re.MULTILINE,
)


def preferred_time_token(value: str, unit: str) -> str:
    base = TIME_UNIT_BASE[unit.lower()]
    plural = "" if value == "1" else "s"
    return "{value} {unit}".format(value=value, unit=base + plural)


def html_subscript_formula(formula: str) -> str:
    return re.sub(r"(\d+)", r"<sub>\1</sub>", formula)


def apply_regex_substitution(
    text: str,
    pattern: re.Pattern,
    replacer: Callable[[Match[str]], str],
) -> str:
    return pattern.sub(lambda match: replacer(match), text)


def normalize_note_label(match: Match[str]) -> str:
    label = match.group("label")
    body = match.group("body").strip()
    normalized_label = "NOTE" if label == "NOTE" else label
    if body:
        return "{indent}> **{label}:** {body}".format(
            indent=match.group("indent"),
            label=normalized_label,
            body=body,
        )

    return "{indent}> **{label}:**".format(
        indent=match.group("indent"),
        label=normalized_label,
    )


def fix_readme_style(readme: str) -> str:
    fixed = readme

    fixed = apply_regex_substitution(
        fixed,
        PH_RE,
        lambda match: "pH {value}".format(value=match.group("value")),
    )
    fixed = apply_regex_substitution(
        fixed,
        UNICODE_SUBSCRIPT_RE,
        lambda match: (
            html_subscript_formula(match.group("formula").translate(UNICODE_SUBSCRIPT_MAP))
            if any(char in "₀₁₂₃₄₅₆₇₈₉" for char in match.group("formula"))
            else match.group(0)
        ),
    )
    fixed = apply_regex_substitution(
        fixed,
        CHEMICAL_FORMULA_RE,
        lambda match: (
            html_subscript_formula(match.group("formula"))
            if any(char.isdigit() for char in match.group("formula"))
            else match.group(0)
        ),
    )
    fixed = apply_regex_substitution(
        fixed,
        TEMPERATURE_RE,
        lambda match: "{value} °C".format(value=match.group("value")),
    )
    fixed = apply_regex_substitution(
        fixed,
        MICRO_UNIT_RE,
        lambda match: "{value} {unit}".format(
            value=match.group("value"),
            unit=PREFERRED_MICRO_UNITS[match.group("unit").lower()],
        ),
    )
    fixed = apply_regex_substitution(
        fixed,
        UNIT_RE,
        lambda match: "{value} {unit}".format(
            value=match.group("value"),
            unit=PREFERRED_UNITS[match.group("unit").lower()],
        ),
    )
    fixed = apply_regex_substitution(
        fixed,
        TIME_RE,
        lambda match: preferred_time_token(match.group("value"), match.group("unit")),
    )
    fixed = apply_regex_substitution(
        fixed,
        NOTE_LABEL_RE,
        normalize_note_label,
    )

    return fixed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply deterministic style fixes to a protocol README.",
    )
    parser.add_argument("readme_path", help="Path to the README.md file to fix.")
    args = parser.parse_args()

    readme_path = Path(args.readme_path)
    original = readme_path.read_text(encoding="utf-8")
    fixed = fix_readme_style(original)

    if fixed == original:
        print("No style changes needed.")
        return

    readme_path.write_text(fixed, encoding="utf-8")
    print("Applied style fixes to {path}.".format(path=readme_path))


if __name__ == "__main__":
    main()

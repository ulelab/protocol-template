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
    rf"\b(?P<value>{NUMBER_RE})(?P<space>\s*)(?P<unit>µL|mL|ml|ML|L|l|µg|mg|g|kg|ng|mM|µM|nM|M)\b"
)
TIME_RE = re.compile(
    rf"\b(?P<value>{NUMBER_RE})(?P<space>\s*)(?P<unit>(?i:seconds?|minutes?|hours?|secs?|mins?|hrs?)|s|h)\b",
)
CHEMICAL_FORMULA_RE = re.compile(
    r"\b(?P<formula>(?:[A-Z][a-z]?\d*){2,})\b"
)
UNICODE_SUBSCRIPT_RE = re.compile(r"\b(?P<formula>[A-Za-z₀₁₂₃₄₅₆₇₈₉]+)\b")
ELEMENT_TOKEN_RE = re.compile(r"[A-Z][a-z]?\d*")

PERIODIC_TABLE_SYMBOLS = {
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
}

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
    "nm": "nM",
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
LITERAL_CHEMICAL_FORMULAS = {
    "ddH2O": "ddH<sub>2</sub>O",
}


def preferred_time_token(value: str, unit: str) -> str:
    base = TIME_UNIT_BASE[unit.lower()]
    plural = "" if value == "1" else "s"
    return f"{value} {base}{plural}"


def html_subscript_formula(formula: str) -> str:
    return re.sub(r"(\d+)", r"<sub>\1</sub>", formula)


def is_word_char(char: str) -> bool:
    return char.isalnum() or char == "_"


def contains_literal_token(text: str, token: str) -> bool:
    start = 0
    while True:
        index = text.find(token, start)
        if index == -1:
            return False

        before = text[index - 1] if index > 0 else ""
        after_index = index + len(token)
        after = text[after_index] if after_index < len(text) else ""
        if (not before or not is_word_char(before)) and (
            not after or not is_word_char(after)
        ):
            return True

        start = index + len(token)


def is_acronym_like_formula(formula: str, token_matches: List[re.Match]) -> bool:
    if any(char.islower() for char in formula) or len(token_matches) < 3:
        return False

    if not token_matches[-1].group(2):
        return False

    uncounted_prefix_tokens = [
        token_match for token_match in token_matches[:-1] if not token_match.group(2)
    ]
    return len(uncounted_prefix_tokens) >= 2


def is_supported_chemical_formula(formula: str) -> bool:
    if not any(char.isdigit() for char in formula):
        return False

    tokens = ELEMENT_TOKEN_RE.findall(formula)
    if not tokens or "".join(tokens) != formula:
        return False

    token_matches = []
    for token in tokens:
        token_match = re.match(r"([A-Z][a-z]?)(\d*)$", token)
        if token_match is None or token_match.group(1) not in PERIODIC_TABLE_SYMBOLS:
            return False
        token_matches.append(token_match)

    if is_acronym_like_formula(formula, token_matches):
        return False

    return True


def format_unit_failure(line_number: int, found: str, preferred: str) -> str:
    if "μ" in found:
        return (
            f"Line {line_number}: unit uses Greek letter mu `μ` (U+03BC); "
            f"copy/paste the micro sign `µ` (U+00B5) in `{preferred}` "
            f"instead of `{found}`."
        )

    return f"Line {line_number}: unit should use `{preferred}` style, found `{found}`."


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
                failures.append(format_unit_failure(line_number, match.group(0), preferred))

        for match in UNIT_RE.finditer(line):
            preferred_unit = PREFERRED_UNITS[match.group("unit").lower()]
            preferred = f"{match.group('value')} {preferred_unit}"
            if match.group(0) != preferred:
                failures.append(format_unit_failure(line_number, match.group(0), preferred))

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

        for found, preferred in LITERAL_CHEMICAL_FORMULAS.items():
            if contains_literal_token(line, found):
                failures.append(
                    f"Line {line_number}: chemical formula should use `{preferred}` style, found `{found}`."
                )

        for match in CHEMICAL_FORMULA_RE.finditer(line):
            formula = match.group("formula")
            if "<sub>" in formula or not is_supported_chemical_formula(formula):
                continue

            preferred = html_subscript_formula(formula)
            if formula != preferred:
                failures.append(
                    f"Line {line_number}: chemical formula should use `{preferred}` style, found `{formula}`."
                )

        for match in UNICODE_SUBSCRIPT_RE.finditer(line):
            formula = match.group("formula")
            if not any(char in "₀₁₂₃₄₅₆₇₈₉" for char in formula):
                continue

            normalized = formula.translate(UNICODE_SUBSCRIPT_MAP)
            if not is_supported_chemical_formula(normalized):
                continue
            preferred = html_subscript_formula(normalized)
            failures.append(
                f"Line {line_number}: chemical formula should use `{preferred}` style, found `{formula}`."
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

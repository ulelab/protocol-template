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


def preferred_time_token(value: str, unit: str) -> str:
    base = TIME_UNIT_BASE[unit.lower()]
    plural = "" if value == "1" else "s"
    return f"{value} {base}{plural}"


def html_subscript_formula(formula: str) -> str:
    return re.sub(r"(\d+)", r"<sub>\1</sub>", formula)


def is_supported_chemical_formula(formula: str) -> bool:
    if not any(char.isdigit() for char in formula):
        return False

    tokens = ELEMENT_TOKEN_RE.findall(formula)
    if not tokens or "".join(tokens) != formula:
        return False

    return all(
        re.match(r"([A-Z][a-z]?)(\d*)$", token) is not None
        and re.match(r"([A-Z][a-z]?)(\d*)$", token).group(1) in PERIODIC_TABLE_SYMBOLS
        for token in tokens
    )


def format_unit_failure(line_number: int, found: str, preferred: str) -> str:
    if "μ" in found:
        return (
            f"Line {line_number}: unit uses Greek mu `μ`; use the micro sign `µ` "
            f"in `{preferred}` instead of `{found}`."
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

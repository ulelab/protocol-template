"""Backward-compatible entrypoint for protocol README validation."""

from pathlib import Path
import sys
from typing import List

try:
    from scripts.validate_protocol_content import validate_readme as validate_content
    from scripts.validate_protocol_style import validate_readme_style
except ModuleNotFoundError:
    from validate_protocol_content import validate_readme as validate_content
    from validate_protocol_style import validate_readme_style


def validate_readme(readme: str) -> List[str]:
    return list(dict.fromkeys(validate_content(readme) + validate_readme_style(readme)))


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

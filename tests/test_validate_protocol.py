"""Tests for the protocol README validator."""

import unittest

from scripts.validate_protocol import validate_readme


VALID_README = """# RNA extraction

### Status: 🟢 `[OK]` | validated and ready to use
| ***Status legend***: | 🟢 `[OK]` working | 🟡 `[?]` unconfirmed / partial | 🔴 `[X]` broken |
|---|---|---|---|

# About

Extract total RNA from cultured cells.

## Contents
1. [Lysis](#1-lysis)
2. [Cleanup](#2-cleanup)

# 1. Lysis

Add 10 uL lysis buffer and incubate for 5 min at 20 C.

# 2. Cleanup

Wash with 70% ethanol and elute.
"""

TEMPLATE_NOTE = "> Template repository: Click `Use this template` to create a new protocol repo. Template docs are in [docs/USING_THIS_TEMPLATE.md](https://github.com/ulelab/protocol-template/blob/main/docs/USING_THIS_TEMPLATE.md)\n\n"


class ValidateReadmeTests(unittest.TestCase):
    def test_valid_readme_passes(self) -> None:
        self.assertEqual(validate_readme(VALID_README), [])

    def test_missing_protocol_title_before_about_fails(self) -> None:
        readme = VALID_README.replace("# RNA extraction\n\n", "", 1)
        self.assertIn(
            "Missing top-level protocol title before '# About'.",
            validate_readme(readme),
        )

    def test_placeholder_step_headings_and_contents_are_reported(self) -> None:
        readme = VALID_README.replace("[Lysis](#1-lysis)", "[Step 1](#1-step-1)", 1)
        readme = readme.replace("# 1. Lysis", "# 1. Step 1", 1)

        failures = validate_readme(readme)

        self.assertIn(
            "Found placeholder step heading: # 1. Step 1",
            failures,
        )
        self.assertIn(
            "Found placeholder contents entry: 1. [Step 1](#1-step-1)",
            failures,
        )

    def test_source_token_matching_normalizes_micro_symbol(self) -> None:
        source = "Use 10 µL reagent for 5 min at 20 C and finish in 70% ethanol."
        self.assertEqual(validate_readme(VALID_README, source), [])

    def test_source_token_matching_allows_spacing_and_unit_normalization(self) -> None:
        source = "Use 1uL primer, 20ul water, incubate 10min at 65C, then hold 30min at 42  C."
        readme = VALID_README.replace(
            "Add 10 uL lysis buffer and incubate for 5 min at 20 C.",
            "Add 1 µL primer and 20 µL water, incubate for 10 minutes at 65 °C, then hold for 30 minutes at 42 °C.",
            1,
        )
        self.assertEqual(validate_readme(readme, source), [])

    def test_missing_status_line_is_reported(self) -> None:
        readme = VALID_README.replace(
            "### Status: 🟢 `[OK]` | validated and ready to use\n",
            "",
            1,
        )
        self.assertIn(
            "Missing or malformed status line: expected '### Status: ...'.",
            validate_readme(readme),
        )

    def test_template_repository_note_must_be_removed(self) -> None:
        readme = TEMPLATE_NOTE + VALID_README
        self.assertIn(
            f"Found template-only text that must be removed: {TEMPLATE_NOTE.strip()}",
            validate_readme(readme),
        )


if __name__ == "__main__":
    unittest.main()

"""Tests for the protocol README style validator."""

import unittest

from scripts.validate_protocol_style import validate_readme_style


VALID_README = """# RNA extraction

### Status: 🟢 `[OK]` | validated and ready to use
| ***Status legend***: | 🟢 `[OK]` working | 🟡 `[?]` unconfirmed / partial | 🔴 `[X]` broken |
|---|---|---|---|

# About

Extract total RNA from cultured cells.

## Contents
1. [Lysis](#1-lysis)
2. [Cleanup](#2-cleanup)
3. [Materials](#3-materials)

# 1. Lysis

Add 10 µL lysis buffer and incubate for 5 minutes at 20 °C.
Adjust to pH 7.4 with 1 mM Tris-HCl.
Prepare with H<sub>2</sub>O and MgCl<sub>2</sub>.

# 2. Cleanup

Wash with ethanol and elute.

# 3. Materials

- 10 µL pipette
- 1 mM Tris-HCl
"""


class ValidateReadmeStyleTests(unittest.TestCase):
    def test_valid_readme_passes(self) -> None:
        self.assertEqual(validate_readme_style(VALID_README), [])

    def test_volume_and_time_formatting_are_reported(self) -> None:
        readme = VALID_README.replace(
            "Add 10 µL lysis buffer and incubate for 5 minutes at 20 °C.",
            "Add 10uL lysis buffer and incubate for 5 min at 20 °C.",
            1,
        )

        failures = validate_readme_style(readme)

        self.assertTrue(
            any("unit should use `10 µL` style" in failure for failure in failures)
        )
        self.assertTrue(
            any(
                "time should use full-word units like `5 minutes`" in failure
                for failure in failures
            )
        )

    def test_temperature_formatting_is_reported(self) -> None:
        readme = VALID_README.replace("20 °C", "20C", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any("temperature should use `20 °C` style" in failure for failure in failures)
        )

    def test_micro_sign_and_unit_case_are_reported(self) -> None:
        readme = VALID_README.replace("1 mM Tris-HCl", "1uM Tris-HCl", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any("unit should use `1 µM` style" in failure for failure in failures)
        )

    def test_greek_mu_is_reported_and_normalized_to_micro_sign(self) -> None:
        readme = VALID_README.replace("10 µL lysis buffer", "10 μL lysis buffer", 1)
        readme = readme.replace("10 µL pipette", "10 μL pipette", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any(
                "unit uses Greek mu `μ`; use the micro sign `µ`" in failure
                for failure in failures
            )
        )

    def test_ph_spacing_and_case_are_reported(self) -> None:
        readme = VALID_README.replace("pH 7.4", "PH7.4", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any("pH should use `pH 7.4` style" in failure for failure in failures)
        )

    def test_plain_chemical_formula_uses_html_subscripts(self) -> None:
        readme = VALID_README.replace("H<sub>2</sub>O", "H2O", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any(
                "chemical formula should use `H<sub>2</sub>O` style" in failure
                for failure in failures
            )
        )

    def test_unicode_subscript_formula_is_reported(self) -> None:
        readme = VALID_README.replace("MgCl<sub>2</sub>", "MgCl₂", 1)

        failures = validate_readme_style(readme)

        self.assertTrue(
            any(
                "chemical formula should use `MgCl<sub>2</sub>` style" in failure
                for failure in failures
            )
        )

    def test_non_chemical_abbreviation_with_digits_is_not_reported(self) -> None:
        readme = VALID_README + "\nHold at RT1 before proceeding.\nThen move to RT₁ if needed.\n"

        failures = validate_readme_style(readme)

        self.assertFalse(any("RT<sub>1</sub>" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()

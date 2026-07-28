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
Dilute primer to 25 nM.
Prepare with H<sub>2</sub>O and MgCl<sub>2</sub>.

# 2. Cleanup

Wash with ethanol and elute.

# 3. Materials

- 10 µL pipette
- 1 mM Tris-HCl
- 25 nM primer
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

    def test_uppercase_biology_and_figure_labels_are_not_time_units(self) -> None:
        readme = (
            VALID_README
            + "\nMeasure 25S rRNA and 3S RNA.\n"
            + "See Supplementary Figure 1S, Figure 2H, and Table 2H.\n"
        )

        failures = validate_readme_style(readme)

        self.assertFalse(any("25 seconds" in failure for failure in failures))
        self.assertFalse(any("3 seconds" in failure for failure in failures))
        self.assertFalse(any("1 second" in failure for failure in failures))
        self.assertFalse(any("2 hours" in failure for failure in failures))

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
                "unit uses Greek letter mu `μ` (U+03BC); copy/paste the micro sign `µ` (U+00B5)"
                in failure
                for failure in failures
            )
        )

    def test_greek_mu_unit_reports_one_copyable_message_per_token(self) -> None:
        cases = [
            ("10 μL lysis buffer", "10 µL", "10 μL"),
            ("1 μM primer", "1 µM", "1 μM"),
            ("2 μg enzyme", "2 µg", "2 μg"),
        ]

        for readme, preferred, found in cases:
            with self.subTest(found=found):
                failures = validate_readme_style(readme)

                self.assertEqual(
                    failures,
                    [
                        "Line 1: unit uses Greek letter mu `μ` (U+03BC); "
                        "copy/paste the micro sign `µ` (U+00B5) in "
                        f"`{preferred}` instead of `{found}`."
                    ],
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

    def test_ddh2o_uses_html_subscript(self) -> None:
        readme = VALID_README + "\nRinse with ddH2O before storage.\n"

        failures = validate_readme_style(readme)

        self.assertTrue(
            any(
                "chemical formula should use `ddH<sub>2</sub>O` style"
                in failure
                for failure in failures
            )
        )

    def test_ddh2o_substring_is_not_reported(self) -> None:
        readme = VALID_README + "\nKeep the addH2O helper label unchanged.\n"

        failures = validate_readme_style(readme)

        self.assertFalse(any("ddH<sub>2</sub>O" in failure for failure in failures))

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

    def test_bioinformatics_acronyms_with_digits_are_not_chemical_formulas(self) -> None:
        readme = (
            VALID_README
            + "\nCompare CHIP3, FISH3, and NGS2 annotations before ChIP-seq.\n"
        )

        failures = validate_readme_style(readme)

        self.assertFalse(any("CHIP<sub>3</sub>" in failure for failure in failures))
        self.assertFalse(any("FISH<sub>3</sub>" in failure for failure in failures))
        self.assertFalse(any("NGS<sub>2</sub>" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()

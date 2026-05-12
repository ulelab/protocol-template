"""Tests for the protocol README style fixer."""

import unittest

from scripts.fix_protocol_style import fix_readme_style


class FixReadmeStyleTests(unittest.TestCase):
    def test_fixer_normalizes_supported_style_issues(self) -> None:
        original = """# RNA extraction

Add 10uL lysis buffer and incubate for 5 min at 20C.
Adjust to PH7.4 with 1uM primer in H2O and MgCl₂.
"""
        expected = """# RNA extraction

Add 10 µL lysis buffer and incubate for 5 minutes at 20 °C.
Adjust to pH 7.4 with 1 µM primer in H<sub>2</sub>O and MgCl<sub>2</sub>.
"""

        self.assertEqual(fix_readme_style(original), expected)

    def test_fixer_normalizes_greek_mu_and_note_labels(self) -> None:
        original = """NB: Keep samples cold.
Use 10 μL enzyme, then wait 1hr.
"""
        expected = """> **NB:** Keep samples cold.
Use 10 µL enzyme, then wait 1 hour.
"""

        self.assertEqual(fix_readme_style(original), expected)

    def test_fixer_does_not_subscript_non_chemical_product_codes(self) -> None:
        readme = """# Reagents

- Totalpure NGS/Ampure XP beads
- 20 µM Cas9 Nuclease, S. pyogenes (M0386T)
- 20 µM Cas9 Nuclease, S. pyogenes (M₀₃₈₆T)
"""

        self.assertEqual(fix_readme_style(readme), readme)

    def test_fixer_is_idempotent(self) -> None:
        readme = """# RNA extraction

> **Note:** Keep samples cold.
Use 10 µL reagent with 25 nM primer for 5 minutes at 37 °C in H<sub>2</sub>O.
"""

        self.assertEqual(fix_readme_style(fix_readme_style(readme)), readme)


if __name__ == "__main__":
    unittest.main()

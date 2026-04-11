Convert `legacy/source.txt` into `README.md`.

Use the existing `README.md` as the target template and structure.

Also read and follow `.github/copilot-instructions.md`.
Apply those instructions even if you are not GitHub Copilot.

Use `legacy/source.txt` as the primary source.
Also check the PDF file in the `legacy/` folder as the reference source, especially for tables, layout-dependent content, and anything unclear.

Requirements:
1. Preserve all protocol content.
2. Do not change scientific meaning.
3. Do not invent missing information.
4. Keep exact reagent names, quantities, temperatures, timings, and conditions unless only formatting is being normalized.
5. Normalize only safe formatting, such as:
   - adding a space between numbers and units
   - using `seconds`, `minutes`, `hours`
   - using `µL`, `mL`, `L`
   - using `37 °C` style temperature formatting
6. Preserve the step order from the source.
7. Do not delete repeated warnings or notes.
8. If any text does not fit cleanly into the template, place it under `# Migration notes` or `## Unplaced content`.
9. Mark uncertainty with `CHECK:` instead of guessing.
10. After drafting, add a short summary in `# Migration notes` covering:
   - formatting normalizations performed
   - ambiguities and uncertainty flagged
   - content placed in `## Unplaced content`

Only edit `README.md`.

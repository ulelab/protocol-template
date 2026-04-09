Migrate `legacy/source.txt` into `README.md` using `TEMPLATE.md` as the target structure.

Requirements:
1. Preserve all protocol content.
2. Do not change scientific meaning.
3. Do not invent missing information.
4. Keep exact reagent names, quantities, temperatures, and timings unless only formatting is normalized.
5. Normalize only safe surface formatting:
   - add space between numbers and units
   - use `seconds`, `minutes`, `hours`
   - use `µL`, `mL`, `L`
   - use `°C` with a preceding space before the unit, e.g. `37 °C`
6. If any source text does not clearly fit a template section, place it in `# Migration notes` or `## Unplaced content`.
7. Mark ambiguity with `CHECK:`.
8. Do not delete repeated warnings or notes.
9. Preserve step order from the source.
10. After drafting, include a short migration summary in `# Migration notes` listing:
   - formatting normalizations performed
   - ambiguities flagged
   - content placed in `## Unplaced content`

Only edit `README.md`.
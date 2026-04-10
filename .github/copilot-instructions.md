# Living Protocols repository instructions

This repository stores laboratory protocols in Markdown in `README.md`.

## Primary rule
Do not change protocol meaning.

## Migration behavior
When converting legacy protocol text into the repository template:

- Preserve all procedural content, warnings, notes, reagent names, quantities, timings, temperatures, and conditions, preserving their location.
- Do not invent missing values or steps.
- Do not delete any content from the source.
- Do not silently summarize, compress, or merge steps.
- If text does not map cleanly into the template, place it under `# Migration notes` or `## Unplaced content`.
- If any interpretation is uncertain, mark it with `CHECK:` rather than guessing.
- Preserve exact reagent and equipment names unless only formatting is changing.

## Allowed formatting normalization
You may normalize formatting only when the meaning is unchanged and unambiguous:
- Add a space between numbers and units.
- Standardize temperature formatting to `37 °C`.
- Standardize volume units to `µL`, `mL`, `L`.
- Standardize concentration units to `mM`, `µM`, `nM`, `% (w/v)`, etc.
- Standardize time units to full words: `seconds`, `minutes`, `hours`.
- Standarize chemical names to match the source but with consistent formatting (e.g. `Tris-HCl` instead of `Tris HCl`).
- Standardize pH formatting to `pH 7.4`.
- Standardize `H2O` to `H₂O`. Similarly for other chemical formulas.
- Normalize bullet formatting and markdown table formatting.
- Normalize heading structure to match the repository template.
- For reaction mixes and anything tabular, place them inside a table as in template.
- Normalize markdown headings, bullets, and tables
- Notes start with `> **Note**` and are placed immediately after the step they refer to, or at the end of the protocol if they clearly refer to the whole protocol.
- Remove empty columns from tables.

## Disallowed changes
- Do not infer omitted concentrations, times, temperatures, or volumes.
- Do not convert `overnight`, `RT`, `briefly`, `room temperature` or similar vague language into precise values.
- Do not reorder steps unless the source clearly numbers them in that order.
- Do not remove duplicate-looking content unless it is truly identical and both copies are preserved in review notes.
- Do not rewrite scientific wording for style if that risks changing meaning.
- Do not infer values for missing quantities.
- Do not replace vague language with precise values.
- Do not try to calculate or infer values that are not explicitly stated.
- Do not fill in table cells with values that are missing from the source.
- Do not replace one reagent name with another.
- Do not remove repeated warnings or notes.
- Do not omit unmapped text.

## Output requirements
When drafting a migrated protocol:
- Use the template headings exactly.
- Use the template headings in `README.md`
- Keep all source content.
- Add `CHECK:` markers for uncertainty.
- Add an `# Migration notes` section listing:
  - template metadata from `template-metadata.yml`
  - ambiguous mappings
  - normalized formatting changes
  - content copied verbatim but not confidently placed



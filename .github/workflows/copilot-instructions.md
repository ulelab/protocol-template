# Living Protocols repository instructions

This repository stores laboratory protocols in Markdown in `README.md`.


## Primary rule
Do not change protocol meaning.

## Migration behavior
When converting legacy protocol text into the repository template:

- Preserve all procedural content, warnings, notes, reagent names, quantities, timings, temperatures, and conditions.
- Do not invent missing values.
- Do not delete any content from the source.
- Do not silently summarize, compress, or merge steps.
- If text does not map cleanly into the template, place it under `# Migration notes` or `## Unplaced content`.
- If any interpretation is uncertain, mark it with `CHECK:` rather than guessing.
- Preserve exact reagent and equipment names unless only formatting is changing.

## Allowed formatting normalization
You may normalize formatting only when the meaning is unchanged and unambiguous:
- add a space between numbers and units
- standardize temperature formatting to `37 °C`
- standardize volume units to `µL`, `mL`, `L`
- standardize time units to full words: `seconds`, `minutes`, `hours`
- normalize bullet formatting and markdown table formatting
- normalize heading structure to match the repository template
- for reaction mixes and anything tabular, place them inside a table as in template
- normalize markdown headings, bullets, and tables

## Disallowed changes
- Do not infer omitted concentrations, times, temperatures, or volumes.
- Do not convert `overnight`, `RT`, `briefly`, `room temperature` or similar vague language into precise values.
- Do not reorder steps unless the source clearly numbers them in that order.
- Do not remove duplicate-looking content unless it is truly identical and both copies are preserved in review notes.
- Do not rewrite scientific wording for style if that risks changing meaning.
- Do not infer values for missing quantities
- Do not replace one reagent name with another
- Do not remove repeated warnings or notes
- Do not omit unmapped text

## Output requirements
When drafting a migrated protocol:
- Use the template headings exactly.
- Use the template headings in `README.md`
- Keep all source content.
- Add `CHECK:` markers for uncertainty.
- Add an `# Migration notes` section listing:
  - ambiguous mappings
  - normalized formatting changes
  - content copied verbatim but not confidently placed



---
name: protocol-migration
description: Convert legacy/source.txt into README.md using the repository template, preserving scientific meaning and marking uncertainty with CHECK:.
---

Use this skill when migrating a legacy protocol into this repository template.

Goal:
Convert `legacy/source.txt` into `README.md`, using the existing `README.md` as the target template and structure.

Primary sources:
- `legacy/source.txt` is the main source
- also consult the PDF in `legacy/` for tables, layout-dependent content, and anything unclear

Core rules:
- Do not change protocol meaning
- Do not invent missing information
- Do not delete source content
- Do not silently summarize, compress, or merge steps
- Preserve exact reagent names, quantities, timings, temperatures, and conditions unless only formatting is being normalized
- Preserve step order unless the source clearly indicates otherwise
- If anything is uncertain, mark it with `CHECK:` instead of guessing

If content does not fit cleanly:
- place it under `# Migration notes` or `## Unplaced content`

Allowed formatting normalization only when meaning is unchanged:
- add a space between numbers and units
- standardize temperature formatting to `37 °C`
- standardize volumes to `µL`, `mL`, `L`
- standardize concentrations to `mM`, `µM`, `nM`, `% (w/v)`
- standardize time units to `seconds`, `minutes`, `hours`
- standardize pH formatting to `pH 7.4`
- normalize bullets, headings, and markdown tables to match the template
- use tables for reaction mixes and other tabular content
- use HTML subscripts for chemical formulas where needed
- normalize note-like text to blockquote style, e.g. `> **Note**`

Do not:
- infer omitted values
- replace vague wording like `overnight` or `room temperature` with precise values
- reorder steps unless clearly justified by the source
- remove repeated warnings or notes
- replace one reagent with another
- omit unmapped text

Output requirements:
- edit `README.md`
- use the template headings
- keep the template badge at the top
- remove the template instruction note
- add `# Migration notes` including:
  - imported protocol metadata from `source-metadata.yml` if present
  - template metadata from `template-metadata.yml`
  - ambiguous mappings
  - formatting normalizations performed
  - content copied verbatim but not confidently placed

After drafting, verify the migration against the source:
- compare the migrated `README.md` against `legacy/source.txt`
- - compare the migrated `README.md` against the PDF in `legacy/`
- check that all protocol steps, notes, warnings, reagent names, quantities, temperatures, timings, and conditions are still present
- check that no source content has been silently omitted, merged, or reordered without justification
- check any tables, layout-dependent content, or ambiguous sections against the PDF in `legacy/`
- leave `CHECK:` anywhere the mapping is uncertain rather than guessing

Verification checklist:
- `README.md` still matches the scientific content of `legacy/source.txt`
- no protocol steps or warnings were omitted
- no values were invented or made more precise than in the source
- tables and layout-dependent content were checked against the PDF in `legacy/`
- any uncertain mappings are marked with `CHECK:`
- any meaningful normalization choices are noted in `# Migration notes`

Prefer preserving meaning over making the output prettier.
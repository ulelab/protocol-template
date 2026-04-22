# Living Protocols repository instructions

This repository stores laboratory protocols in Markdown in `README.md`.

## Primary rule
Do not change protocol meaning.
Use `legacy/source.md` as the primary source when rewriting `README.md`.
Use `legacy/source.txt` only as a fallback when `legacy/source.md` looks malformed, incomplete, or unclear.
Use the PDF file in `legacy/` as the final reference source of truth for tables, figures, layout-dependent content, and anything still ambiguous.
If `legacy/source.md` and `legacy/source.txt` disagree, prefer `legacy/source.md` for general structure and prose, but use the original PDF as the final tie-breaker.

## Migration behavior
When converting legacy protocol content into the repository template:

- Preserve all protocol content.
- Preserve all procedural content, warnings, notes, reagent names, quantities, timings, temperatures, and conditions, preserving their location.
- Do not change scientific meaning.
- Do not invent missing information.
- Do not invent missing values or steps.
- Do not delete any content from the source.
- Do not silently summarize, compress, or merge steps.
- Keep exact reagent names, quantities, temperatures, timings, and conditions unless only formatting is being normalized.
- If text does not map cleanly into the template, place it under `# Migration notes` or `## Unplaced content`.
- If any interpretation is uncertain, mark it with `CHECK:` rather than guessing.
- Do not delete repeated warnings or notes.
- Preserve the step order from the source unless the source clearly indicates otherwise.
- Preserve exact reagent and equipment names unless only formatting is changing.

## Allowed formatting normalization
You may normalize formatting only when the meaning is unchanged and unambiguous:
- Add a space between numbers and units.
- Standardize temperature formatting to `37 °C`.
- Standardize volume units to `µL`, `mL`, `L`, using the micro sign `µ` consistently.
- Standardize concentration units to `mM`, `µM`, `nM`, `% (w/v)`, etc., using the micro sign `µ` consistently.
- Standardize time units to full words: `seconds`, `minutes`, `hours`.
- Standardize chemical names to match the source but with consistent formatting (e.g. `Tris-HCl` instead of `Tris HCl`).
- Standardize pH formatting to `pH 7.4`.
- Standardize chemical formulas with HTML subscripts, for example H2O to H<sub>2</sub>O. Similarly for other chemical formulas (e.g. MgCl2 to MgCl<sub>2</sub>).
- Do not use Unicode subscript characters such as `₂`.
- Standardize `RNAseq` or `RNA-Seq` to `RNA-seq`. Same for `ChIP-seq`, `ATAC-seq`, etc.
- Normalize bullet formatting and markdown table formatting.
- Normalize heading structure to match the repository template.
- For reaction mixes and anything tabular, place them inside a table as in template.
- Normalize markdown headings, bullets, and tables.
- "Note" or "NOTE" or "Optional" or "Recommended" or "Warning" are normalized to start with `>` (example `> **Note**`) and are placed immediately after the step they refer to, or at the end of the protocol if they clearly refer to the whole protocol.
- Remove empty columns from tables.
- Synchronize `Contents` with actual headings in the protocol.

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
- Use the template headings in `README.md`.
- Keep all source content.
- Add `CHECK:` markers for uncertainty.
- Use `CHECK:` only for genuine unresolved uncertainty. If no uncertainty remains, do not mention `CHECK:` at all.
- Add an `# Migration notes` section listing:
  - formatting normalizations performed
  - ambiguities and uncertainty flagged
  - content placed in `## Unplaced content`
  - Imported protocol metadata from `source-metadata.yml` (only the non-blank lines).
  - Imported protocol metadata from `source-metadata.yml` if present.
  - template_version from `template-metadata.yml`.
  - ambiguous mappings.
  - normalized formatting changes.
  - content copied verbatim but not confidently placed.
- Keep ![Created with ulelab Protocol Template](https://img.shields.io/badge/created%20with-ulelab%20Protocol%20Template-blue) at the top of the file.
- Delete the "Template repository: Click `Use this template` to create a new protocol repo..." note.
- Remove the template instruction note.

## Verification
After drafting, verify the migration against the source:

- compare the migrated `README.md` against `legacy/source.md`
- compare any malformed, incomplete, or ambiguous passages against `legacy/source.txt`
- compare the migrated `README.md` against the PDF in `legacy/` for tables, figures, layout-dependent content, and any remaining ambiguity
- check that all protocol steps, notes, warnings, reagent names, quantities, temperatures, timings, and conditions are still present
- check that no source content has been silently omitted, merged, or reordered without justification
- check any tables, layout-dependent content, or ambiguous sections against the PDF in `legacy/`
- leave `CHECK:` anywhere the mapping is uncertain rather than guessing

Verification checklist:
- `README.md` still matches the scientific content of `legacy/source.md`
- any malformed, incomplete, or ambiguous passages were cross-checked against `legacy/source.txt`
- no protocol steps or warnings were omitted
- no values were invented or made more precise than in the source
- tables and layout-dependent content were checked against the PDF in `legacy/`
- any uncertain mappings are marked with `CHECK:`
- any meaningful normalization choices are noted in `# Migration notes`

Prefer preserving meaning over making the output prettier.

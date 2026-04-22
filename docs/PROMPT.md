Convert `legacy/source.md` into `README.md`.

Use the existing `README.md` as the target template and structure.

Also read and follow `.github/copilot-instructions.md`.
Apply those instructions even if you are not GitHub Copilot.

## Primary rule
Do not change protocol meaning.
Use `legacy/source.md` as the primary source when rewriting `README.md`.
Use `legacy/source.txt` only as a fallback when `legacy/source.md` looks malformed, incomplete, or unclear.
Use the PDF file in `legacy/` as the final reference source of truth for tables, figures, layout-dependent content, and anything still ambiguous after checking the generated text sources.
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
- Preserve exact reagent and equipment names unless only formatting is changing.
- Preserve the step order from the source unless the source clearly indicates otherwise.
- Do not delete repeated warnings or notes.
- If any text does not fit cleanly into the template, place it under `# Migration notes` or `## Unplaced content`.
- Mark uncertainty with `CHECK:` instead of guessing.

## Allowed formatting normalization
Normalize formatting only when the meaning is unchanged and unambiguous:

- add a space between numbers and units
- use `seconds`, `minutes`, `hours`
- use `µL`, `mL`, `L`
- use `37 °C` style temperature formatting
- standardize concentration units to `mM`, `µM`, `nM`, `% (w/v)`, etc., using the micro sign `µ` consistently
- standardize pH formatting to `pH 7.4`
- standardize chemical names to match the source but with consistent formatting, for example `Tris-HCl` instead of `Tris HCl`
- standardize chemical formulas with HTML subscripts, for example H2O to H<sub>2</sub>O and MgCl2 to MgCl<sub>2</sub>
- do not use Unicode subscript characters such as `₂`
- standardize `RNAseq` or `RNA-Seq` to `RNA-seq`, and similarly for `ChIP-seq`, `ATAC-seq`, and related names
- normalize bullets, headings, and markdown tables to match the repository template
- use tables for reaction mixes and other tabular content
- normalize note-like text to blockquote style, for example `> **Note**`
- place note-like text immediately after the step it refers to, or at the end of the protocol if it clearly refers to the whole protocol
- remove empty columns from tables
- synchronize `Contents` with the actual headings in the protocol

## Disallowed changes
- do not infer omitted concentrations, times, temperatures, or volumes
- do not infer values for missing quantities
- do not try to calculate or infer values that are not explicitly stated
- do not convert `overnight`, `RT`, `briefly`, `room temperature`, or similar vague language into precise values
- do not replace vague language with precise values
- do not reorder steps unless the source clearly numbers them in that order
- do not remove duplicate-looking content unless it is truly identical and both copies are preserved in review notes
- do not rewrite scientific wording for style if that risks changing meaning
- do not fill in table cells with values that are missing from the source
- do not replace one reagent name with another
- do not remove repeated warnings or notes
- do not omit unmapped text

## Output requirements
- Only edit `README.md`.
- Use the template headings exactly.
- Use the template headings in `README.md`.
- Keep all source content.
- Add `CHECK:` markers for uncertainty.
- Use `CHECK:` only for genuine unresolved uncertainty. If no uncertainty remains, do not mention `CHECK:` at all.
- Add an `# Migration notes` section.
- After drafting, add a short summary in `# Migration notes` covering:
  - formatting normalizations performed
  - ambiguities and uncertainty flagged
  - content placed in `## Unplaced content`
- Include the following in `# Migration notes`:
  - imported protocol metadata from `source-metadata.yml` if present
  - imported protocol metadata from `source-metadata.yml` using only the non-blank lines
  - template_version from `template-metadata.yml`
  - ambiguous mappings
  - normalized formatting changes
  - content copied verbatim but not confidently placed
- Keep ![Created with ulelab Protocol Template](https://img.shields.io/badge/created%20with-ulelab%20Protocol%20Template-blue) at the top of the file.
- Remove the template instruction note.
- Delete the "Template repository: Click `Use this template` to create a new protocol repo..." note.

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

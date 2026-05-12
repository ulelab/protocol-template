# How to use this template

This repository is a template for creating a new protocol repository.

Do not edit this repository directly unless you are maintaining the template itself.

Instead, create a new repository from this template and edit that new repository.

If you are new to GitHub, start with this short [GitHub Hello World tutorial](https://docs.github.com/en/get-started/start-your-journey/hello-world).


## Contents

- [Create a new protocol repository](#create-a-new-protocol-repository)
  - [1. Add and update a protocol manually](#1-add-and-update-a-protocol-manually)
  - [2. Add and update a protocol from a legacy PDF using GitHub Actions and AI assistance](#2-add-and-update-a-protocol-from-a-legacy-pdf-using-github-actions-and-ai-assistance)
  - [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
- [Validate and fix protocol style](#validate-and-fix-protocol-style)
- [Make changes to an existing protocol](#make-changes-to-an-existing-protocol)
- [Use the protocol in the lab](#use-the-protocol-in-the-lab)
- [Release a protocol](#release-a-protocol)
---

# Create a new protocol repository

1. Open this template repository on GitHub: https://github.com/ulelab/protocol-template
2. Click **Use this template**.
3. Click **Create a new repository**.
4. Choose a repository name. Use a short, clear name starting with `protocol-`.
   > Example: `protocol-rnaseq`
5. Choose the `lab protocols` custom property, if used in your organisation.
6. Choose where to create the repository.
7. Click **Create repository**.

You now have your own copy of the template.

The structure of the template is:
```md
.
├── .github
│   ├── workflows/              # Automation for validations and PDF generation
│   └── copilot-instructions.md # AI-assisted migration instructions
├── docs
│   ├── PROMPT.md               # AI migration prompt
│   ├── USING_THIS_TEMPLATE.md  # Usage guide for this protocol template
│   └── template-metadata.yml   # Template metadata
├── legacy
│   └── source-metadata.yml     # [EDIT THIS] Source metadata
├── scripts/                    # Scripts used by GitHub Actions
├── tests/                      # Tests for the protocol validator
├── CODEOWNERS                  # GitHub handles of protocol maintainers
└── README.md                   # [EDIT THIS] Protocol file (initially placeholders)
```

The main file you must edit for protocol content is `README.md`. **Do not rename** this file. For migration, you will also upload a PDF in `legacy/`. It's recommended to also fill in `source-metadata.yml` and `CODEOWNERS`.
> **Warning**: Do not edit any other files unless you want to change template mechanics themselves; that is an advanced action.

#### To proceed, choose one of the following routes:

- [1. Add and update a protocol manually](#1-add-and-update-a-protocol-manually): Useful if you write a protocol from scratch, editing the `README.md` directly.
- [2. Add and update a protocol from a legacy PDF using GitHub Actions and AI assistance](#2-add-and-update-a-protocol-from-a-legacy-pdf-using-github-actions-and-ai-assistance): Useful for one-time conversion from a legacy source.

---

## 1. Add and update a protocol manually

### Suggested step-by-step workflow

1. Create a new repository from the template (see [Create a new protocol repository](#create-a-new-protocol-repository)).
2. Create and switch to a new branch named e.g. `import-protocol`. Do not work on `main` directly for adding protocols.
3. Edit `README.md` on GitHub or locally (after cloning the repo in a code editor such as [VS Code](https://code.visualstudio.com/)) on the `import-protocol` branch.
> **Note**: Alternatively, you can complete steps 3-8 in GitHub Codespaces. On GitHub.com select the branch you want to work on, click **Code**, go to **Codespaces** tab and click **Create codespace on import-protocol**. This will open VS Code in a new browser tab, with all files loaded automatically. Note that this uses GitHub-hosted compute, and free usage is limited.

> **Recommended**: Also fill in the `source-metadata.yml`, even if not fully. Helps track source protocol provenance.

4. Replace all template text with real content.
5. Delete sections you do not need.
6. Check that no `TODO` text remains.
7. Follow the guidelines in [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
8. Commit your changes, then push.
> **Important**: Before making any further local changes after pushing, run `git pull`. GitHub Actions may have added a new commit on your branch.
> **Recommended**: After pushing your changes, go to the GitHub **Actions** tab on your protocol's repo page, and manually run the `validate-protocol-README` workflow. In the **Use workflow from** branch menu, select your own working branch, for example `import-protocol`. This will validate the `README.md` file, or flag content and formatting errors. If there are problems, this check will fail, and the error messages will point you to the specific issues that need addressing. This workflow does not check whether the scientific content is correct.

9. Once you are happy with the result and you've thoroughly checked the created protocol is correct, open a pull request from `import-protocol` into `main`.
10. The validation GitHub Actions workflow (`validate-protocol-README`) will automatically run on that pull request when `README.md` has changed. It runs a content check for the required title, status line, status legend, key headings, unresolved placeholders, and placeholder step names, plus a style check for unit formatting. If checks fail, fix them before merging into `main`.
11. Ask for a reviewer where possible.

> **Review scope**: Before opening the pull request, check the changed files. For a routine protocol edit, only `README.md` or `CODEOWNERS` should change. This does not apply to the one-time legacy PDF import workflow, where files in `legacy/` may also be created or updated. If any other files changed, remove those changes or explain clearly why they are needed.

> **Note**: Always check accuracy and make sure required sections, such as protocol status and the status legend, are present.

---

## 2. Add and update a protocol from a legacy PDF using GitHub Actions and AI assistance

This repository includes tools to help convert legacy protocol PDFs into Markdown.

This route can save time. It helps keep the template structure consistent, normalizes formatting, standardizes units where this can be done without changing meaning, and highlights parts of the source protocol that need manual review.

> **Important**: This route is AI-assisted, not AI-reliant. Always compare the generated `README.md` against the original PDF before merging. Every migration must be checked by the person carrying it out and by a separate reviewer before it is merged into `main`.

### Suggested step-by-step workflow

1. Create a new repository from the template.
2. Create and switch to a new branch named e.g. `import-protocol`. Do not work on `main` directly for importing protocols.
3. Upload the legacy PDF to the `legacy` folder, then commit and push it.
> **Important**: Please use a high-quality, well-structured protocol as the source. Only one PDF file per protocol is supported.

> **Warning**: Custom content in protocols may represent a challenge for this route. The extraction workflows may create protocol-relevant image files, such as table images, figures, diagrams, or visual instructions, in `legacy/images/`. During the README migration, these should either be converted to Markdown when legible and unambiguous, or retained in `README.md` at the correct location. We strongly recommend that you check these types of elements were handled correctly.

> **Recommended**: Also fill in the `source-metadata.yml`, even if not fully. Helps track source protocol provenance.
4. Keep **exactly one PDF** in the `legacy` folder, otherwise the process will fail.
5. Once you push a PDF change in the `legacy` folder to a non-`main` branch, the migration GitHub Actions will run automatically. `pdf-to-text` writes `legacy/source.txt`, and `pdf-to-markdown` writes `legacy/source.md` and may write extracted images to `legacy/images/`. Check that these files were created before the next step.
> **Note**: If these files were not created within a few minutes, check whether a GitHub Action has failed (`Actions` tab). Manually re-run the failed workflow, or re-run both `pdf-to-text` and `pdf-to-markdown` if you are unsure which one failed. If it still fails, check the error and ask the template maintainers for help.

6. Clone the repo locally, and switch to `import-protocol` branch. If you already have a local clone, run `git pull` to get the latest changes locally.
> **Note**: Alternatively, you can complete steps 6-16 in GitHub Codespaces. On GitHub.com select the branch you want to work on, click **Code**, go to **Codespaces** tab and click **Create codespace on import-protocol**. This will open VS Code in a new browser tab, with all files loaded automatically. Note that this uses GitHub-hosted compute, and free usage is limited.
7. Open the repo folder in a code editor and use GitHub Copilot or another LLM assistant. We recommend [VS Code](https://code.visualstudio.com/).
8. Use the `protocol-migration` skill (or if you prefer, paste the prompt in `docs/PROMPT.md`) to ask GitHub Copilot or another LLM to rewrite `README.md`. The model will also follow the repository instructions in [`../.github/copilot-instructions.md`](../.github/copilot-instructions.md). This will edit the `README.md` file in-place, using `legacy/source.md` as the primary source, `legacy/source.txt` as a fallback when needed, extracted images in `legacy/images/` as protocol content to review, and the legacy PDF as the final tie-breaker for tables, figures, and unclear layout-dependent content.
> **Note**: Use the best model you have access to. We tested capability with the Copilot Free Usage plan, and it works reasonably well, but advanced models will likely work even better, especially with more difficult documents.

> **Note**: The initial migration request asks the model to perform the mandatory image/table pass and convert legible image-based tables to Markdown during the first draft. If some images are left unconverted, resolve them manually or ask an LLM to attempt the conversion.

**In VS Code**:
  - **Codex**: use `/skills` and select the `protocol-migration` skill, or enter `$protocol-migration` in the Codex chat input box.
  - **Claude Code**: enter `/protocol-migration`, or ask it to use the `protocol-migration` skill.
  - **Copilot agent mode**: ask it to use the `protocol-migration` skill (e.g. something like:
  `Migrate this protocol using the protocol-migration skill.`)

9. Review the changes. If most of them look reasonable, commit with a message like `migration by LLM`. Do not push yet at this stage.
10. Verify that `README.md` is accurate by comparing it to the original PDF and fix mistakes.
11. Check the `Migration notes` section and every place marked with `CHECK:`.
12. Confirm that protocol-relevant extracted images were converted to Markdown tables where possible, or retained as images.
13. Make any changes necessary. Delete sections you do not need.
14. Check that no `TODO` text remains.
15. Follow the guidelines in [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
> **Note**: Steps 10-15 can be either performed manually or by further prompting the LLM in your code editor or VS Code.

16. Commit your changes, then push.
> **Important**: Before making any further local changes after pushing, run `git pull`. GitHub Actions will have added a new commit on your branch with a PDF version of `README.md`.
> **Recommended**: After pushing your changes, go to the GitHub **Actions** tab on your protocol's repo page, and manually run the `validate-protocol-README` workflow. In the **Use workflow from** branch menu, select your own working branch, for example `import-protocol`. This will validate the `README.md` file, or flag content and formatting errors. If there are problems, this check will fail, and the error messages will point you to the specific issues that need addressing. This workflow does not check whether the scientific content is correct.

17. Once you are happy with the result and you've thoroughly checked the created protocol is correct, open a pull request from `import-protocol` into `main`.
18. The validation GitHub Actions workflow (`validate-protocol-README`) will automatically run on that pull request when `README.md` has changed. It runs a content check for the required title, status line, status legend, key headings, unresolved placeholders, and placeholder step names, plus a style check for unit formatting. If checks fail, fix them *before* merging into `main`.
19. Ask for a reviewer where possible.

> **Review scope**: Before opening the pull request, check the changed files. For a legacy PDF import pull request, expected changes are `README.md`, `CODEOWNERS`, and files in `legacy/`, such as `legacy/source-metadata.yml`, the source PDF, `legacy/source.txt`, `legacy/source.md`, or `legacy/images/`. If any other files changed, remove those changes or explain clearly why they are needed.

---

## 3. General guidelines for the protocol file (`README.md`)

This section applies whether you updated the protocol manually or generated it from a legacy PDF.

#### Minimum content every protocol should have

**At minimum, make sure your protocol includes:**

- a clear title, formatted as a top-level Markdown heading using a single `#`, for example `# RNA-seq`
- an accurate `### Status:` line
- a status legend row containing `[OK]`, `[?]`, and `[X]`
- a short description (`# About`)
- contents (`## Contents`)
- a materials section (`# ... Materials`)
These are mandatory items for validation.

Recommended content:

- the starting material
- the actual steps
- key reagents, volumes, and timings
- notes or warnings if something is easy to get wrong

#### What to change

Modify:

- `TODO: Protocol title`
- all other `TODO` entries
- the status line, according to the legend
- the step names
- the notes, tables, and reagent details
- any table placement or layout that needs adjusting

Fill in:

- the protocol title
- a short description in `# About`
- all protocol steps
- reagents, volumes, and conditions
- QC or output information if needed

#### What to delete

Delete anything you do not need.

The template is intentionally generic.

#### What not to leave in

Before finishing, search `README.md` for:

- `TODO`
- `Optional sub-step`
- placeholder text such as `Step 1` and `Step 2`
- unresolved `CHECK:`

These should usually be replaced or deleted.

#### How to update the status

At the top of the file, update the status line.

Available statuses:

- 🟢 `[OK]` = working
- 🟡 `[?]` = unconfirmed / partial
- 🔴 `[X]` = broken / do not use

Examples:

```md
### Status: 🟢 `[OK]` | validated and ready to use
### Status: 🟡 `[?]` | draft, needs testing
### Status: 🔴 `[X]` | do not use, conditions still under review
```

---

# Validate and fix protocol style

You can manually run protocol validation at any time from the GitHub **Actions** tab:

1. Open **Actions**.
2. Select the `validate-protocol-README` workflow.
3. Click **Run workflow**.
4. In the **Use workflow from** branch menu, select your own working branch, for example `import-protocol`, unless you are intentionally validating another branch.
5. Click **Run workflow** and read the result.

If validation fails, fix the reported problems on your branch, commit, push, and run validation again.

**Optional**: if validation reports unit or notation style issues, you can ask GitHub to open an automated style-fix pull request:

1. Open **Actions**.
2. Select the `fix-protocol-style` workflow.
3. Click **Run workflow**.
4. In the **Use workflow from** branch menu, choose the branch whose workflow file should run. If you are unsure, use `main`.
5. In `base_branch`, enter the branch that contains the `README.md` you want to fix, for example `import-protocol`.
6. Click **Run workflow**.

The `fix-protocol-style` workflow applies deterministic formatting fixes, then opens a new pull request back into the `base_branch` you entered. Review that pull request before merging it. This workflow does not check whether the scientific content is correct.

---

# Make changes to an existing protocol

If you want to adapt or improve an existing protocol on GitHub:

1. Create a new branch from `main`, or from another branch you want to build on.
2. Do not work directly on `main`.
3. Changes should go into `main` through a pull request.
4. Edit `README.md`.
5. Commit small, clear changes.
6. Make sure the commit message explains what changed.
7. If the change relates to a GitHub Issue, include the Issue number, for example `closes #12`.
8. After pushing to any branch, wait a few minutes.
9. GitHub will automatically generate a PDF version of the protocol on that branch.
10. If the PDF is not generated within a few minutes (you may need to refresh the page), go to the GitHub **Actions** tab, manually run the `README-to-pdf` workflow, and select your working branch in the **Use workflow from** branch menu.
11. PDF generation creates another commit, usually with a message like `Update <repo-name>.pdf`.
12. Before making any further local changes after pushing, run `git pull`. GitHub Actions may have added a new commit on your branch.
13. If you have questions about a protocol, or want to propose a change, open a GitHub Issue using the `Protocol issues` template and assign relevant people.
14. If you are developing a protocol as a team, you can use a GitHub Project.
15. Use Issues to track optimisation ideas or questions.
16. Add images, gels, notes or links to code or data to the relevant Issue.
17. Close the Issue when the question is resolved.
18. This helps keep a record of what has already been tried.
19. If your change should become part of the main protocol, open a pull request to `main` and request review from relevant people.
20. Before requesting review, check the changed files. For a routine protocol edit, only `README.md` or `CODEOWNERS` should change. For a legacy PDF import, files in `legacy/` may also be created or updated. If any other files changed, remove those changes or explain clearly why they are needed.
21. Do not merge into `main` without review, unless you are the only person using that protocol.

---

# Use the protocol in the lab

### Always use the PDF that matches the protocol version you want

After pushing changes to `README.md`, wait a few minutes.

GitHub will automatically generate a PDF version of the protocol on that branch and commit it back to the repository, usually with a message like `Update <repo-name>.pdf`.

If the PDF is not generated within a few minutes, go to the GitHub **Actions** tab, manually run the `README-to-pdf` workflow, and select your working branch in the **Use workflow from** branch menu.

Before making any further local changes after pushing, run `git pull`. GitHub Actions may have added a new commit on your branch.

### Use the commit SHA as the version identifier

The PDF includes a short commit SHA in its header.

Treat that commit SHA as the identifier of the protocol version you are using in the lab.

That SHA tells you exactly which `README.md` version was used to generate the PDF.

Always check that the commit SHA printed on the PDF matches the exact protocol version you want to use.

### Checks to do before using a protocol

Before using a protocol in the lab, check all of the following:
- `README.md` is accurate
- the commit SHA printed on the PDF matches the protocol version you intend to use
- the protocol status
- any `CHECK:` items or migration uncertainties have been resolved

---

# Release a protocol

Once a protocol has been added and confirmed to be working — that is, its status is 🟢 `[OK]` and this is clearly marked at the top of the file, create the first release: `1.0.0`.
> **Recommended**: Link releases to Zenodo if you want each protocol version to have a citable DOI.

Further changes can then be released using semantic versioning. Ensure maintainers listed in `CODEOWNERS` and other protocol developers and users are involved or aware if a new version release is planned.

---

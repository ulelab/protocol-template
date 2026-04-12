# How to use this template

This repository is a template for creating a new protocol repository.

Do not edit this repository directly unless you are maintaining the template itself.

Instead, create a new repository from this template and edit that new repository.

## Contents

- [Create a new protocol repository](#create-a-new-protocol-repository)
  - [1. Add and update a protocol manually](#1-add-and-update-a-protocol-manually)
  - [2. Add and update a protocol from a legacy PDF using GitHub Actions and Copilot](#2-add-and-update-a-protocol-from-a-legacy-pdf-using-github-actions-and-copilot)
  - [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
- [How to make changes to a protocol](#how-to-make-changes-to-a-protocol)
- [Using the protocol in the lab](#using-the-protocol-in-the-lab)
- [Release a protocol](#release-a-protocol)
---

# Create a new protocol repository

1. Open this template repository on GitHub: https://github.com/ulelab/Protocol_template
2. Click **Use this template**.
3. Click **Create a new repository**.
4. Choose a repository name.
   Example: `Protocol_iCLIP`
   Use a short, clear name starting with `Protocol_`.
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
├── CODEOWNERS                  # GitHub handles of protocol maintainers
└── README.md                   # [EDIT THIS] Protocol file (initially placeholders)
```

The only file you must modify is `README.md`. It's recommended to also fill in `source-metadata.yml` and `CODEOWNERS`.

#### To proceed, choose one of the following routes:

- [1. Add and update a protocol manually](#1-add-and-update-a-protocol-manually): Useful if you write a protocol from scratch, editing the `README.md` directly.
- [2. Add and update a protocol from a legacy PDF using GitHub Actions and Copilot](#2-add-and-update-a-protocol-from-a-legacy-pdf-using-github-actions-and-copilot): Useful for one-time conversion from a legacy source.

---

## 1. Add and update a protocol manually

### Suggested workflow

1. Create a new repository from the template (see above).
2. Make and switch to a new branch named `import-protocol`. **DO NOT** use a different name for this branch.
3. Edit `README.md` on GitHub or locally (after cloning the repo) on the `import-protocol` branch.
> **Recommended**: Also fill in the `source-metadata.yml`, even if not fully. Helps track source protocol provenance.
4. Replace all template text with real content.
5. Delete sections you do not need.
6. Check that no `TODO` text remains.
7. Follow the guidelines in [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
8. Commit your changes, then push.
9. Pushing to `import-protocol` will trigger a GitHub Actions workflow that checks `README.md` for formatting errors. If there are problems, this check will fail.
10. If checks fail, fix them before trying to merge into `main`.
11. Once all checks pass and you are happy with the result, open a pull request from `import-protocol` into `main`. This will re-trigger the validation CI test. Ask for a reviewer.

> **Note:** Always check accuracy and make sure required sections, such as protocol status and the status legend, are present.


---

## 2. Add and update a protocol from a legacy PDF using GitHub Actions and Copilot

This repository also includes tools to help convert legacy protocol PDFs into Markdown.

This route can save time. It helps keep the template structure consistent, normalizes formatting, standardizes units where this can be done without changing meaning, and highlights parts of the source protocol that need manual review.

> **Important:** This route is AI-assisted, not AI-reliant. Always compare the generated `README.md` against the original PDF before merging. Every migration must be checked by the person carrying it out and by a separate reviewer before it is merged into `main`.

### Suggested workflow

1. Create a new repository from the template.
2. Make and switch to a new branch named `import-protocol`. **DO NOT** use a different name for this branch.
3. Upload the legacy PDF to the `legacy` folder, then commit and push it.
> **Recommended**: Also fill in the `source-metadata.yml`, even if not fully. Helps track source protocol provenance.
4. Keep exactly one PDF in the `legacy` folder, otherwise the process will fail.
5. Once you push to `import-protocol`, the `prepare migration` GitHub Action will run. This will extract the PDF text and write `legacy/source.txt`. Check this text file was created before the next step.
6. Run `git pull` to get the latest changes locally.
7. Use the prompt in `docs/PROMPT.md` to ask GitHub Copilot or another LLM to rewrite `README.md`. The model will also follow the repository instructions in [`.github/copilot-instructions.md`](.github/copilot-instructions.md). This will edit the `README.md` file in-place.
> **Note:**: Use the best model you have access to. We tested capability with the Copilot Free Usage plan, and it works reasonably well, but advanced models will likely work even better.
8. Review the changes. If most of them look reasonable, commit with a message like `migration by LLM`.
9. Verify that `README.md` is accurate by comparing it to the original PDF.
10. Check the `Migration notes` section and every place marked with `CHECK:`. Resolve anything unclear.
11. Make any changes necessary. Delete sections you do not need.
12. Check that no `TODO` text remains.
13. Follow the guidelines in [3. General guidelines for the protocol file (`README.md`)](#3-general-guidelines-for-the-protocol-file-readmemd)
14. Commit your changes, then push.
15. Pushing to `import-protocol` will trigger a GitHub Actions workflow that checks `README.md` for formatting and units errors. If there are problems, this check will fail.
16. If checks fail, fix them before trying to merge into `main`.
17. Once all checks pass and you are happy with the result, open a pull request from `import-protocol` into `main`. This will re-trigger the verification CI test. Ask for a reviewer.

---

## 3. General guidelines for the protocol file (`README.md`)

This section applies whether you updated the protocol manually or generated it from a legacy PDF.

#### Minimum content every protocol should have

At minimum, make sure your protocol includes:

- a clear title
- an accurate status
- a short description
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
- a short description in **About**
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


### Common mistakes

#### I edited the template repository itself

Do not do that unless you are updating the master template for everyone.

Create a new repository from the template instead.

#### I left `TODO` text in the file

Search the file for `TODO` and replace or delete all of it.

#### I left headings like `Step 1` and `Step 2`

Rename them to real step names.

Example:

- `Step 1` -> `RNA extraction`
- `Step 2` -> `Fragmentation`
- `Step 3` -> `Reverse transcription`

---

# How to make changes to a protocol

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
10. This creates another commit, usually with a message like `Update Protocol_x.pdf`.
11. If you have questions about a protocol, open a GitHub Issue and assign relevant people.
12. If you are developing a protocol as a team, you can use a GitHub Project.
13. Use Issues to track optimisation ideas or questions.
14. Add images, gels, notes or links to code or data to the relevant Issue.
15. Close the Issue when the question is resolved.
16. This helps keep a record of what has already been tried.
17. If your change should become part of the main protocol, open a pull request to `main` and request review from relevant people.
18. Do not merge into `main` without review, unless you are the only person using that protocol.

---

# Using the protocol in the lab

### Always use the PDF that matches the protocol version you want

After pushing changes to `README.md`, wait a few minutes.

GitHub will automatically generate a PDF version of the protocol on that branch and commit it back to the repository, usually with a message like `Update Protocol_x.pdf`.

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

Further changes can then be released using semantic versioning. Ensure maintainers listed in `CODEOWNERS` are involved or aware if a new version release is planned.

---

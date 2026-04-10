# How to use this template

This repository is a template for creating a new protocol repository.

Do not edit this repository directly unless you are maintaining the template itself.

Instead, create a new repository from this template and edit that new repository.
---

# Create a new protocol repository

1. Open this template repository on GitHub: https://github.com/ulelab/Protocol_template
2. Click **Use this template**.
3. Click **Create a new repository**.
4. Choose a repository name.
   Example: `Protocol_iCLIP`
   Use a short, clear name starting with `Protocol_`.
5. Choose the `lab protocols` custom property.
6. Choose where to create the repository.
7. Click **Create repository**.

You now have your own copy of the template.

Next, choose one of the following routes:

- [1. Add and update a protocol manually](#1-add-and-update-a-protocol-manually)
- [2. Add and update a protocol from a legacy PDF using GitHub Actions and Copilot](#2-add-and-update-a-protocol-from-a-legacy-pdf-using-github-actions-and-copilot)

---

## 1. Add and update a protocol manually

### Suggested workflow

1. Create a new repository from the template (see above).
2. Make and switch to a new branch named `migration`.
3. Edit `README.md` on GitHub or locally on the `migration` branch.
4. Replace all template text with real content.
5. Delete sections you do not need.
6. Check that no `TODO` text remains.
7. Follow the guidelines in [`3. General guidelines for `README.md``](#3-general-guidelines-for-readmemd)
8. When done, delete `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf`.
9. Commit your changes, then push.
10. Pushing to `migration` will trigger a GitHub Actions workflow that lints `README.md`. If there are problems, this check will fail.
11. If checks fail, fix them before trying to merge into `main`.
12. Once all checks pass and you are happy with the result, open a pull request from `migration` into `main`. This will re-trigger the verification CI test. Ask for a reviewer.
13. Before taking the protocol to the lab, see [3. Taking the protocol to the lab / using it](#3-taking-the-protocol-to-the-lab--using-it).

> **Note:** Always check accuracy and make sure required sections, such as protocol status and the status legend, are present.


---

## 2. Add and update a protocol from a legacy PDF using GitHub Actions and Copilot

This repository also includes tools to help convert legacy protocol PDFs into Markdown.

This route can save a significant amount of time. It also helps keep the template structure consistent, normalizes formatting, standardizes units where appropriate, and can highlight unclear parts of the source protocol.

> **Important:** This route is AI-assisted, not AI-reliant. Always compare the generated `README.md` against the original PDF before merging. Migration must be checked by the person carrying it out and by a separate reviewer.

### Suggested workflow

1. Create a new repository from the template.
2. Make and switch to a new branch named `migration`.
3. Upload the legacy PDF to the `legacy` folder, then commit and push it.
4. Keep exactly one PDF in that folder when you run the workflow.
5. Run the `prepare migration` GitHub Action. This will extract the PDF text and write `legacy/source.txt`.
6. Run `git pull` to get the latest changes locally.
7. Use the prompt in `PROMPT.md` to ask GitHub Copilot to rewrite `README.md` using `legacy/source.txt`. Copilot will also follow the repository instructions in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).
8. Verify that `README.md` is accurate by comparing it to the original PDF.
9. Check the `Migration notes` section and every place marked with `CHECK:`. Resolve anything unclear.
10. Delete sections you do not need.
11. Check that no `TODO` text remains.
12. Follow the guidelines in [`3. General guidelines for `README.md``](#3-general-guidelines-for-readmemd)
13. When done, delete `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf`.
14. Commit your changes, then push.
15. Pushing to `migration` will trigger a GitHub Actions workflow that lints `README.md`. If there are problems, this check will fail.
16. If checks fail, fix them before trying to merge into `main`.
17. Once all checks pass and you are happy with the result, open a pull request from `migration` into `main`. This will re-trigger the verification CI test. Ask for a reviewer.
18. Before taking the protocol to the lab, see [3. Taking the protocol to the lab / using it](#3-taking-the-protocol-to-the-lab--using-it).

---

## 3. General guidelines for `README.md`

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

#### Minimum content every protocol should have

At minimum, make sure your protocol includes:

- a clear title
- an accurate status
- a short description
- the starting material
- the actual steps
- key reagents, volumes, and timings
- notes or warnings if something is easy to get wrong

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

If you want to adapt or improve a protocol:

1. Create a new branch from `main`, or from another branch you want to build on.
2. Do not work directly on `main`.
3. Changes should go into `main` through a pull request.
4. Edit `README.md`.
5. Commit small, clear changes.
6. Make sure the commit message explains what changed.
7. If the change relates to a GitHub Issue, include the Issue number, for example `closes #12`.
8. After pushing to any branch, wait a few minutes.
9. GitHub will automatically generate a PDF version of the protocol on that branch.
10. This creates another commit, usually with a message like `chore: update Protocol_x.pdf`.
11. Always use the newest PDF that matches your changes.
12. Always check that the commit SHA printed on the PDF matches the exact protocol version you want to use. See also [3. Taking the protocol to the lab / using it](#3-taking-the-protocol-to-the-lab--using-it).
13. If you have questions about a protocol, open a GitHub Issue and assign relevant people.
14. If you are developing a protocol as a team, you can use a GitHub Project.
15. Use Issues to track optimisation ideas or questions.
16. Add images, gels, or notes to the relevant Issue.
17. Close the Issue when the question is resolved.
18. This helps keep a record of what has already been tried.
19. If your change should become part of the main protocol, open a pull request to `main` and request review from relevant people.
20. Do not merge into `main` without review, unless you are the only person using that protocol.

---

# Taking the protocol to the lab

This section applies whether you updated the protocol manually or generated it from a legacy PDF.

### Use the PDF that matches the protocol version you want

After pushing changes to `README.md`, wait a few minutes.

GitHub will automatically generate a PDF version of the protocol on that branch and commit it back to the repository, usually with a message like `chore: update Protocol_x.pdf`.

Always use the PDF that matches the intended `README.md`.

### Use the commit SHA as the version identifier

The PDF includes a short commit SHA in its header.

Treat that commit SHA as the identifier of the protocol version you are using in the lab.

That SHA tells you exactly which `README.md` version was used to generate the PDF.

Always check that the commit SHA printed on the PDF matches the exact protocol version you want to use.

### Checks to do before using a protocol

Before using a protocol in the lab, check all of the following:
- the commit SHA printed on the PDF matches the protocol version you intend to use
- `README.md` is accurate
- the protocol status
- any `CHECK:` items or migration uncertainties have been resolved

---


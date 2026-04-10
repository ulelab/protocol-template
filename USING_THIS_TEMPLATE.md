# How to use this template

This repository is a **template** for adding a new protocol.

Do **not** edit this template repository directly unless you are maintaining the template itself.

Instead, create your **own new repository from this template**, then edit that new repository.

---

## 1. Make a new protocol repository

1. Open this template repository on GitHub (https://github.com/ulelab/Protocol_template).
2. Click **Use this template**.
3. Click **Create a new repository**.
4. Choose a repository name.
   - Example: `Protocol_iCLIP`
   - Use short, clear names, starting with "Protocol_".
5. Choose the `lab protocols` custom property.
6. Choose where to create it.
7. Click **Create repository**.

You now have your own copy of the template.

---

## 2. How to add and update a protocol

Open the new repository, create a new branch named `migration` and edit the protocol file (`README.md`).

### Suggested workflow

1. Create a new repository from the template.
2. Make and switch to a new branch named `migration`
3. Edit the protocol file on GitHub or locally on the `migration` branch.
4. Replace all template text with real content.
5. Delete sections you do not need.
6. Check that no `TODO` text remains.
7. When done, delete the `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf` files.
8. Commit your changes, then push.
9. The push on `migration` will trigger a GitHub actions workflow that will lint `README.md`. If there are problems, this check will fail.
10. If you have failing checks, fix them before trying to merge your changes into `main`.
11. Once all checks pass and you are happy, open a pull request from `migration` into `main`. This will re-trigger the verification CI test. Ask for a reviewer.

> **Note**: Always check the accuracy and that required sections (like protocol status and legend) are present.

## General guidelines for the protocol file `README.md`

### What to change

Modify:
- `TODO: Protocol title`
- all other `TODO` entries
- the status line, according to the legend
- the step names
- the notes, tables, and reagent details
- feel free to move tables etc. around

Fill in:
- protocol title
- short description in **About**
- all protocol steps
- reagents / volumes / conditions
- QC or output information if needed
---

### What to delete

Delete anything you do not need.
The template is intentionally generic.

---

### What not to leave in

Before finishing, search the file for:

- `TODO`
- `Optional sub-step`
- placeholder text like `Step 1`, `Step 2`

These should usually be replaced or deleted.

---

### How to update the status

At the top of the file, change the status line.

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

### Minimum things every protocol should have

At minimum, make sure your protocol includes:

- a clear title
- an accurate status
- a short description
- the starting material
- the actual steps
- key reagents / volumes / timings
- notes or warnings if something is easy to get wrong

### Common mistakes

#### I edited the template repository itself

Do not do that unless you are updating the master template for everyone.

Create a new repository from the template instead.

#### I left `TODO` everywhere

Search the file for `TODO` and replace or delete all of them.

#### I left headings like `Step 1` and `Step 2`

Rename them to real step names.

Example:

- `Step 1` → `RNA extraction`
- `Step 2` → `Fragmentation`
- `Step 3` → `Reverse transcription`

## 3. AI-assisted production of the protocol file `README.md`

We also provide tools to automate the transition from existing legacy protocols in PDF formats to Markdown.
Going this route will save significant amount of time, and also ensures the template structure is followed, formatting normalised, units of measurement are standardised, etc. In practice, we have also learnt this route can identify things that are unclear in the protocols.

> **Important**: This route is AI-assisted, not AI-reliant. **Always check the accuracy** of the `README.md` by comparing it to your original protocol PDF. Also check that required sections (like protocol status and legend) are present. Migration should not be completed and merged into `main` unless it was verified by humans: the person in charge of the migration, and a different person who acts as the reviewer of the pull request from `migration` into `main`.

### Suggested workflow

1. Create a new repository from the template.
2. Make and switch to a new branch named `migration`
3. Edit the protocol file on GitHub or locally on the `migration` branch.
4. Automated replacement of template text with real content using GitHub actions and LLMs:
   4.1 Upload your protocol PDF inside the `legacy` folder, commit and push. 
   4.2 Run the `prepare migration` GitHub Action: this will make a text file based on the PDF.
   4.3 Once the txt file is succesfully produced, `git pull` the latest changes locally.
   4.4 Use the prompt in `PROMPT.md` to ask GitHub Copilot to edit the `README.md` while converting the txt content to Markdown. Copilot will also use the instructions in [`copilot-instructions.md`](https://github.com/ulelab/Protocol_template/blob/main/.github/copilot-instructions.md).
   4.5 Verify the `README.md` is accurate by comparing it to the oroginal PDF.
   4.6 Check the `Migration notes` section and all places marked by `CHECK:`. Resolve anything that is unclear.
5. Delete sections you do not need.
6. Check that no `TODO` text remains.
7. When done, delete the `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf` files.
8. Commit your changes, then push.
9. The push on `migration` will trigger a GitHub actions workflow that will lint `README.md`. If there are problems, this check will fail.
10. If you have failing checks, fix them before trying to merge your changes into `main`.
11. Once all checks pass and you are happy, open a pull request from `migration` into `main`. This will re-trigger the verification CI test. Ask for a reviewer.
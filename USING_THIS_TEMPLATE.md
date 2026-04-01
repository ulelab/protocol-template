# How to use this template

This repository is a **template** for adding a new protocol.

Do **not** edit this template repository directly unless you are maintaining the template itself.

Instead, create your **own new repository from this template**, then edit that new repository.

---

## Make a new protocol repository

1. Open this template repository on GitHub (https://github.com/ulelab/Protocol_template).
2. Click **Use this template**.
3. Click **Create a new repository**.
4. Choose a repository name.
   - Example: `Protocol_iCLIP`
   - Use short, clear names, starting with "Protocol_".
5. Choose where to create it.
6. Click **Create repository**.

You now have your own copy of the template.

---

## What to change

1. Delete the `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf` files.
2. Open the new repository and edit the protocol file (`README.md`).

Replace:
- `TODO: Protocol title`
- all other `TODO` entries
- the status line
- the step names
- the notes, tables, and reagent details
- feel free to move tables etc around

Fill in:
- protocol title
- short description in **About**
- all protocol steps
- reagents / volumes / conditions
- QC or output information if needed

> **Note**: if using chatGPT etc to translate your protocol, provide the LLM with the template markdown structure.

---

## What to delete

Delete anything you do not need.

The template is intentionally generic.
It is normal to remove sections.

---

## What not to leave in

Before finishing, search the file for:

- `TODO`
- `Optional sub-step`
- placeholder text like `Step 1`, `Step 2`

These should usually be replaced or deleted.

A finished protocol should not still look like the template.

---

## How to update the status

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

content = """## Minimum things every protocol should have

At minimum, make sure your protocol includes:

- a clear title
- a short description
- the starting material
- the actual steps
- key reagents / volumes / timings
- notes or warnings if something is easy to get wrong
- an accurate status

## Suggested workflow

1. Create a new repository from the template.
2. Edit the protocol file on GitHub or locally.
3. Replace all template text with real content.
4. Delete sections you do not need.
5. Check that no `TODO` text remains.
6. Commit your changes.
7. Ask for review if needed.

## Quick checklist before you finish

- [ ] Protocol title updated
- [ ] Status updated
- [ ] About section filled in
- [ ] Step names updated
- [ ] All `TODO` text removed
- [ ] Unused sections deleted
- [ ] Deletes the `USING_THIS_TEMPLATE.md` and `Protocol_template.pdf` files
- [ ] Volumes / times / temperatures checked
- [ ] Protocol is readable by someone else in the lab

## Common mistakes

### I edited the template repository itself

Do not do that unless you are updating the master template for everyone.

Create a new repository from the template instead.

### I left `TODO` everywhere

Search the file for `TODO` and replace or delete all of them.

### I left headings like `Step 1` and `Step 2`

Rename them to real step names.

Example:

- `Step 1` → `RNA extraction`
- `Step 2` → `Fragmentation`
- `Step 3` → `Reverse transcription`

### My protocol does not need all six steps

That is fine. Delete the unused steps.

### My protocol needs more than six steps

Also fine. Add more sections using the same format.



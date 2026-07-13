# ES POV Customer Demo — Obsidian Vault

Import this folder into your Obsidian vault.

## Obsidian Git: "invalid git repo" fix

The **Obsidian Git** plugin requires a `.git` folder at the **vault root**. This notes folder is only a subdirectory of the `datagen` repo — it does **not** have its own `.git`.

If you opened **only** `ES-POV-Customer-Demo` as your vault, Git will fail. Use one of these fixes:

### Recommended — open the full repo as vault

```bash
git clone https://github.com/fmcghee/datagen.git
cd datagen
git checkout cursor/es-pov-customer-demo-guide-15fc   # or main after PR merge
```

In Obsidian: **Open folder as vault** → select the cloned **`datagen`** folder (repo root, where `.git` lives).

Your notes are at: `obsidian/ES-POV-Customer-Demo/`  
Start at: `obsidian/ES-POV-Customer-Demo/ES POV Customer Demo Guide.md`

Obsidian Git will sync the whole repo (including `docs/`, `datasets/`, etc.).

### Alternative — copy into an existing vault (no Git on this subfolder)

1. Copy `ES-POV-Customer-Demo` into your existing vault.
2. Disable **Obsidian Git** for that vault, or ignore this path — the subfolder is not a git root.

### Alternative — standalone git for notes only

Only if you want this folder as its own repo (not tied to `datagen` PRs):

```bash
cd ES-POV-Customer-Demo
git init
git add .
git commit -m "Initial ES POV demo vault"
```

You would manage remotes/commits separately from `fmcghee/datagen`.

## Quick import (no Git)

1. Copy the `ES-POV-Customer-Demo` folder into your vault root (or open it as a vault).
2. Start at **[[ES POV Customer Demo Guide]]** (map of content).
3. Use the graph view to see links between demo sections.

## Structure

| Note | Purpose |
| --- | --- |
| [[ES POV Customer Demo Guide]] | Main index / MOC |
| [[OmniSphere Credit - Customer Story]] | Customer narrative, pain points, success criteria |
| [[Demo Flow Overview]] | Timing and section order |
| [[01 - Data Readiness]] | Labs 1–3 |
| [[02 - Assets and Identities]] | Labs 4–7 |
| [[03 - Detection Engineering]] | Labs 8–11 |
| [[04 - Threat Intelligence TIM Cloud]] | Labs 12–13 |
| [[05 - Threat Object Enrichment]] | Labs 14–15 |
| [[06 - UEBA Insider Threat]] | Lab 16 |
| [[07 - Incident Management]] | Labs 17–19 |
| [[08 - Automated Email Threat Analysis]] | Lab 20 |
| [[09 - Closing and Next Steps]] | Wrap-up |
| [[Pre-Demo Checklist]] | SA pre-flight |
| [[SPL Reference]] | All validation searches |

## Tags

Notes are tagged for filtering: `#splunk/es`, `#splunk/demo`, `#splunk/pov`, `#splunk/lab201`

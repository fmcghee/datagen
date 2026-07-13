# ES POV Customer Demo — Obsidian Vault

## Fix: Obsidian Git "invalid git repo"

Open this folder **only works with Obsidian Git** if you clone the dedicated vault branch:

```bash
git clone --branch obsidian-vault --single-branch https://github.com/fmcghee/datagen.git es-pov-customer-demo
```

Or from the full repo:

```bash
bash scripts/setup-obsidian-vault.sh ~/Obsidian/es-pov-customer-demo
```

Then in Obsidian: **Open folder as vault** → select the cloned folder.

`.git` is at the vault root — Obsidian Git will work.

---

## If you already have a broken vault folder

1. Note any local edits you made.
2. Remove or rename the old folder.
3. Re-clone with the command above.
4. Re-apply local edits if needed.

---

## Quick start (no Git)

Copy this folder into an existing vault and start at **[[ES POV Customer Demo Guide]]**.

Obsidian Git will not work unless `.git` is at your vault root — use the clone method above instead.

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

`#splunk/es` `#splunk/demo` `#splunk/pov` `#splunk/lab201`

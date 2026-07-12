---
title: "08 - Automated Email Threat Analysis"
tags:
  - splunk/es
  - splunk/demo
  - email-security
  - SAA
lab: "20"
duration: 8 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[07 - Incident Management]]"
next: "[[09 - Closing and Next Steps]]"
---

# §8 — Automated Email Threat Analysis

> [!tip] Talking point
> Cut phishing triage from **45 minutes to minutes**.

Success criterion **5** · Lab 20

## How it works

- **Third-party findings** — SOAR apps ingest directly as ES findings
- **Automated Threat Analysis** (ES 8.5+) — SAA engines (email, web, static/AV)
- Only **malicious** emails remain in email queue after analysis

## Demo steps

1. **Configure → Splunk SOAR → Apps** — filter **Support ES ingestion**
2. **IMAP v2** — `buttercup-security` asset (lab-provided credentials)
3. Ingest settings:
   - Investigation type: `email`
   - Security domain: network
   - Urgency: medium
4. **Poll Now** (max 5) → findings in **User-reported Email Analysis** queue
5. Click finding → **threat analysis** side panel (verdict, score)
6. **Start Investigation → View complete analysis** — full SAA forensics

### Validate

See [[SPL Reference#Email findings count]]

## Customer message

> The platform analyzes reported phish automatically. Analysts only investigate what SAA flags as malicious.

---

← [[07 - Incident Management]] · [[09 - Closing and Next Steps]] →

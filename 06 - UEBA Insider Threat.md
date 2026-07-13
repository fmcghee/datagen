---
title: "06 - UEBA Insider Threat"
tags:
  - splunk/es
  - splunk/demo
  - UEBA
  - insider-threat
lab: "16"
duration: 8 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[05 - Threat Object Enrichment]]"
next: "[[07 - Incident Management]]"
---

# §6 — UEBA & Insider Threat Queue

> [!tip] Talking point
> OmniSphere needs a **separate queue** for insider risk — not mixed with external threat findings.

Success criterion **2** · Lab 16

## Demo steps

1. **Analytics → UEBA** — Top Risky Users (e.g., **JDavis**)
2. User page → **Findings tab** → detection heatmap
3. Explain test mode: `ba_test` index → **Turn on in risk index**
4. Validate — see [[SPL Reference#UEBA risk output]]
5. **Tuning demo:**
   - Entity list: `Jdavis exclusion` (pattern match `jdavis`)
   - Finding exclusion: `UEBA - Detect PowerShell Applications Spawning cmd exe - Rule`
   - Reason: **accepted** (benign)
6. Return to UEBA — excluded detection gone from heatmap
7. **Insider Threat** team queue — `watchlist = true` routing (see [[07 - Incident Management]])

## Customer message

> External attackers and insider risk are different workflows. UEBA routes to a dedicated queue so IR isn't buried in credential-stuffing noise.

---

← [[05 - Threat Object Enrichment]] · [[07 - Incident Management]] →

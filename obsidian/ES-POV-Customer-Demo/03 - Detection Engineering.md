---
title: "03 - Detection Engineering"
tags:
  - splunk/es
  - splunk/demo
  - detections
  - risk-based-alerting
labs: "8-11"
duration: 10 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[02 - Assets and Identities]]"
next: "[[04 - Threat Intelligence TIM Cloud]]"
---

# §3 — Detection Engineering & Risk Index

> [!tip] Talking point
> OmniSphere's biggest pain is noise. ES uses **risk-based alerting** — detections feed the risk index; cumulative risk creates findings.

Success criteria **1, 4** · Labs 8–11 · Adversary: [[OmniSphere Credit - Customer Story#MITRE focus]]

## Detection lifecycle (30 sec)

1. Define objectives
2. Identify requirements
3. Implement, test, validate
4. Continuous tuning
5. Report metrics

## Scattered Spider risk stack

Enable with **risk index output only** (not standalone findings):

| Detection | MITRE | Risk fields |
| --- | --- | --- |
| Detect Mimikatz With PowerShell Script Block Logging | T1003.001 | dest, user_id |
| Malicious PowerShell Process With Obfuscation Techniques | T1059.001 | dest |
| Windows File Download Via PowerShell | T1105 | dest, user |
| Registry Keys Used For Persistence | T1547.001 | dest, user |
| FodHelper UAC Bypass | T1548.002 | dest, user |
| TeamViewer on endpoint | — | per detection |

## Show in UI

1. **Security content → Content management** — filter enabled detections
2. Macro tuning — add `index=win` to PowerShell macro (Lab 8)
3. Noisy detections tuned to **intermediate findings** with low risk:
   - Windows Group Discovery via Net
   - System Information Discovery
4. **Custom detection highlight:** Cisco Secure Endpoint process creation
   - Severity scores: Low=20, Med=30, High=40, Critical=50
   - Eventtype: `se_process_creation`
   - Field aliases on `cisco:se` sourcetype

### Validate

See [[SPL Reference#Risk accumulation]]

## Customer message

> Instead of 500 equal-priority alerts, analysts see risk accumulating. One weak signal is ignored; five signals on the same host becomes a finding.

---

← [[02 - Assets and Identities]] · [[04 - Threat Intelligence TIM Cloud]] →

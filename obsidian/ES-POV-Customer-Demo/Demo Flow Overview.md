---
title: Demo Flow Overview
tags:
  - splunk/demo
  - splunk/pov
parent: "[[ES POV Customer Demo Guide]]"
---

# Demo Flow Overview

```text
OPENING     OmniSphere story + success criteria           (3 min)
§1          Data exploration & CIM readiness              (5 min)  [pre-demo]
§2          Exposure Analytics — assets & identities      (8 min)
§3          Detection engineering & risk index            (10 min)
§4          Threat Intelligence (TIM Cloud)               (10 min)
§5          Threat object enrichment on findings          (8 min)
§6          UEBA — insider threat queue                   (8 min)
§7          Mission Control — queues, investigations, RP  (10 min)
§8          Automated email threat analysis               (8 min)
CLOSE       Outcomes recap + POV next steps                 (3 min)
```

## Section links

| Min | Section | Note |
| ---: | --- | --- |
| 3 | Opening | [[ES POV Customer Demo Guide#Opening script]] |
| 5 | §1 Data | [[01 - Data Readiness]] |
| 8 | §2 Assets | [[02 - Assets and Identities]] |
| 10 | §3 Detections | [[03 - Detection Engineering]] |
| 10 | §4 TIM | [[04 - Threat Intelligence TIM Cloud]] |
| 8 | §5 Enrichment | [[05 - Threat Object Enrichment]] |
| 8 | §6 UEBA | [[06 - UEBA Insider Threat]] |
| 10 | §7 Incidents | [[07 - Incident Management]] |
| 8 | §8 Email | [[08 - Automated Email Threat Analysis]] |
| 3 | Close | [[09 - Closing and Next Steps]] |

## Narrative thread

One story across all sections:

> Analyst sees elevated risk on a host → investigation reveals PowerShell + LSASS activity → TIM enriches file hash → Talos confirms malicious URL → UEBA flags insider pattern on separate queue → email finding auto-analyzed in dedicated queue → investigation closed with response plan documentation.

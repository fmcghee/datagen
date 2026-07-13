---
title: ES POV Customer Demo Guide
tags:
  - splunk/es
  - splunk/demo
  - splunk/pov
  - splunk/lab201
aliases:
  - ES POV Demo
  - OmniSphere Demo
source: ES POV Lab 201 Final Lab Guide
version: "2.0"
created: 2026-07-12
audience: Solution Architects, Sales Engineers, SOC presenters
demo_length: 60-90 min
---

# ES POV Customer Demo Guide

> [!summary] Start here
> Customer-facing proof-of-value demo script from **ES POV Lab 201**, anchored on fictional bank **[[OmniSphere Credit - Customer Story|OmniSphere Credit]]**.

**Recommended length:** 60 min core · 90 min with threat intel + UEBA deep dives

---

## Map of content

### Customer context
- [[OmniSphere Credit - Customer Story]] — industry, pain points, success criteria
- [[Data Sources Reference]] — lab indexes and sourcetypes
- [[Demo Flow Overview]] — timing and narrative arc

### Demo sections (present in order)
1. [[01 - Data Readiness]] — CIM, data models *(5 min, pre-demo)*
2. [[02 - Assets and Identities]] — Exposure Analytics *(8 min)*
3. [[03 - Detection Engineering]] — risk index, Scattered Spider stack *(10 min)*
4. [[04 - Threat Intelligence TIM Cloud]] — TIM sources, threatlists *(10 min)*
5. [[05 - Threat Object Enrichment]] — hashes, URLs, Talos AR *(8 min)*
6. [[06 - UEBA Insider Threat]] — behavioral detections, insider queue *(8 min)*
7. [[07 - Incident Management]] — queues, investigations, response plans *(10 min)*
8. [[08 - Automated Email Threat Analysis]] — IMAP, SAA verdict *(8 min)*
9. [[09 - Closing and Next Steps]] — recap and POV next steps *(3 min)*

### Reference
- [[Pre-Demo Checklist]] — SA pre-flight tasks
- [[SPL Reference]] — all validation searches in one place
- [[Optional Deep Dives]] — appendix topics
- [[Lab Module Map]] — official lab → demo section mapping

---

## Opening script (3 min)

> "OmniSphere Credit is a regional bank evaluating ES Premier after struggling with alert noise in their current SIEM. Their CISO wants faster phishing triage, formal threat intel, insider risk visibility, and documented investigations. Today we'll walk through how ES addresses each of those — using their hybrid environment and the Scattered Spider TTPs they're most worried about."

Show success criteria from [[OmniSphere Credit - Customer Story]] and state what is live vs. pre-staged.

---

## Success criteria quick reference

| # | Criterion | Section |
| --- | --- | --- |
| 1 | Data normalized for ES | [[01 - Data Readiness]] |
| 2 | Insider risk → separate queue | [[06 - UEBA Insider Threat]] |
| 3 | End-to-end investigation | [[07 - Incident Management]] |
| 4 | EDR → risk index | [[03 - Detection Engineering]] |
| 5 | Auto email triage | [[08 - Automated Email Threat Analysis]] |
| 6a | Asset/identity enrichment | [[02 - Assets and Identities]] |
| 6b | IOC enrichment | [[04 - Threat Intelligence TIM Cloud]], [[05 - Threat Object Enrichment]] |

---

## Related

- Source PDF: `ES POV Lab 201 Final Lab Guide`
- Markdown export: `docs/ES-POV-Customer-Demo-Guide.md`
- ServiceNow demo data: `datasets/servicenow/` in datagen repo

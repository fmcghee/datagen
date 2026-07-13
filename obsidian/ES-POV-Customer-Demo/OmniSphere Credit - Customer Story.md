---
title: OmniSphere Credit - Customer Story
tags:
  - splunk/es
  - splunk/demo
  - splunk/pov
  - customer-story
parent: "[[ES POV Customer Demo Guide]]"
---

# OmniSphere Credit — Customer Story

> [!info] Demo anchor
> Use this fictional customer consistently across the entire demo. Back to [[ES POV Customer Demo Guide]].

## Profile

| Attribute | Detail |
| --- | --- |
| Industry | Financial Services — regional bank, ~$8B assets |
| Size | 3,500 employees, 120 branches |
| SOC | 12-person SOC, 2-tier model, 1 content engineer |
| Current state | Splunk Enterprise 3 years; evaluating **ES Premier Cloud** |
| Adversary | **Scattered Spider** |

### MITRE focus (Scattered Spider)

- Phishing — `T1566`
- Create/modify system process — `T1543.003`
- Privilege escalation — `TA0004`

## Business drivers

- Internal audit: slow alert triage, poor incident documentation
- CISO mandate: reduce analyst burnout and MTTR after near-miss phishing
- Core banking modernization needs hybrid security visibility

## Pain points (say these early)

- [ ] Drowning in Sentinel alerts — **no risk prioritization**
- [ ] Manual phishing triage ~45 min per alert
- [ ] No formal threat intel; feeds used ad hoc
- [ ] Insider risk — privileged users accessing customer data
- [ ] Audit gaps on triage time and IR documentation

## Technical success criteria

| # | Success criterion | Demo section |
| --- | --- | --- |
| 1 | Data ingested, normalized, available in dashboards/models/detections | [[01 - Data Readiness]] |
| 2 | Anomalous user behavior → insider threat queue | [[06 - UEBA Insider Threat]] |
| 3 | End-to-end investigation with triage and enrichment | [[07 - Incident Management]] |
| 4 | EDR alerts → intermediate findings in risk index | [[03 - Detection Engineering]] |
| 5 | User-reported email auto-analyzed; malicious only in email queue | [[08 - Automated Email Threat Analysis]] |
| 6a | Asset and identity enrichment on findings | [[02 - Assets and Identities]] |
| 6b | IOC enrichment (URLs, domains, hashes, IPs) | [[04 - Threat Intelligence TIM Cloud]], [[05 - Threat Object Enrichment]] |

## Critical assets & identities (discovery reveal)

- **Assets:** Servers with customer data = highest priority
- **Identities:** Executives = most important identities

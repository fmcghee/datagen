---
title: Pre-Demo Checklist
tags:
  - splunk/es
  - splunk/checklist
  - SA-only
parent: "[[ES POV Customer Demo Guide]]"
---

# Pre-Demo Checklist (SA only)

Run before the customer joins.

## Environment

- [ ] CIM allowlists set for Endpoint (and other used models) — [[01 - Data Readiness]]
- [ ] Data model acceleration verified
- [ ] Exposure Analytics entity sources enabled — [[02 - Assets and Identities]]
- [ ] Risk-index detections enabled (Scattered Spider stack) — [[03 - Detection Engineering]]
- [ ] Cisco Secure Endpoint detection + field aliases configured
- [ ] TIM Cloud sources activated; threatlist active — [[04 - Threat Intelligence TIM Cloud]]
- [ ] Threat object fields on LSASS + BITSAdmin — [[05 - Threat Object Enrichment]]
- [ ] UEBA detections on in risk index — [[06 - UEBA Insider Threat]]
- [ ] Team queues: Email Analysis + Insider Threat — [[07 - Incident Management]]
- [ ] Investigation types + email response plan published
- [ ] IMAP v2 polled; email findings in queue — [[08 - Automated Email Threat Analysis]]
- [ ] Pop-up blocker disabled

## Validation

See [[SPL Reference#Enabled detection count]] — lab expects **14+** enabled detections.

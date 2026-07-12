---
title: "02 - Assets and Identities"
tags:
  - splunk/es
  - splunk/demo
  - exposure-analytics
labs: "4-7"
duration: 8 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[01 - Data Readiness]]"
next: "[[03 - Detection Engineering]]"
---

# §2 — Assets, Identities & Exposure Analytics

> [!tip] Talking point
> Findings are only useful when you know *who* and *what* is at risk.

Success criterion **6a** · Labs 4–7

## Demo steps

1. **Configure → Exposure Analytics → Start setup**
2. **Entity discovery sources → Add:**
   - Okta IM Logs
   - Microsoft Cloud Services Resource
   - Amazon EC2 Instances
   - Linux SSHD Auth Events
   - Microsoft Active Directory
3. Enable **A&I correlation** — Configure → Asset and Identities → Correlation setup

### Identity priority (OmniSphere migration story)

Title-based priority from static identity export:

| Title contains | Priority |
| --- | --- |
| director, vp, chief, ciso, cio, cto | **Critical** |
| manager, supervisor, lead | Medium |
| engineer, developer, analyst, specialist | High |
| sales, hr, recruiter | Low |
| (no title) | Low |

### Region enrichment (acquisition story)

| user_country | user_region |
| --- | --- |
| USA | North America |
| Germany | Europe |

**Configure → Exposure Analytics → Inventory Enrichment → Enrichment Rules**

### Validate

See [[SPL Reference#Identity lookup]]

6. Show asset/identity context changing **urgency** on Mission Control findings

## Customer message

> Exposure Analytics continuously discovers users and assets from your existing logs — no separate CMDB project required. Executive priority and region flow into risk scoring automatically.

---

← [[01 - Data Readiness]] · [[03 - Detection Engineering]] →

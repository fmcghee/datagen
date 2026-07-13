---
title: "07 - Incident Management"
tags:
  - splunk/es
  - splunk/demo
  - mission-control
  - response-plans
labs: "17-19"
duration: 10 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[06 - UEBA Insider Threat]]"
next: "[[08 - Automated Email Threat Analysis]]"
---

# §7 — Incident Management

> [!tip] Talking point
> OmniSphere's audit found poor incident documentation. Mission Control fixes that.

Success criterion **3** · Labs 17–19

## Team queues (Lab 17)

| Queue | Condition | Purpose |
| --- | --- | --- |
| **User-reported Email Analysis** | `incident_origin = IMAP v2 – buttercup-security` | Phishing |
| **Insider Threat** | `watchlist = true` | Insider risk |

**Configure → Findings and investigations → Team queues**

- Roles: `ess_analyst`
- Retention: 7 days archived
- Custom view: **Finding Triage** (threat analysis fields)
- Filter: `threat analysis status = completed`

## Investigation types (Lab 18)

**Configure → Investigation types**

- `email`
- `insider_threat`

## Response plans (Lab 19)

1. **Security content → Response plans**
2. **Workflow Email Phishing Response** (AI-imported from SOP)
3. Assigned to `email` investigation type
4. Walk through tasks on live investigation

## End-to-end workflow

1. **Mission Control → Analyst Queue** — select finding
2. **Assign to me** → **In Progress**
3. **Start investigation** — events, observables, [[04 - Threat Intelligence TIM Cloud|Intelligence tab]]
4. Add note; run AR or playbook
5. Resolve with documentation

## Customer message

> Every investigation has a type, response plan, and team queue. Leadership can audit the process.

---

← [[06 - UEBA Insider Threat]] · [[08 - Automated Email Threat Analysis]] →

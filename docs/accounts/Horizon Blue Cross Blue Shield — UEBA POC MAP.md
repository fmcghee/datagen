# Splunk UEBA Proof of Value
## Horizon Blue Cross Blue Shield of New Jersey

**Document:** Mutual Activity Plan & Success Criteria  
**Environment:** On-prem Splunk Enterprise Security — **Dev**  
**Date:** June 2026  
**Splunk:** Trent Singleton (AE) · Jordan Codrey (SE) · Fred McGhee (SA)  
**Horizon:** Anne Sun · Laurence Klose · Greg Barnes

---

## Purpose

Evaluate **Splunk User and Entity Behavior Analytics (UEBA)** as a native capability within **Splunk Enterprise Security Premier** — replacing parallel Exabeam workflows with behavioral detections, **Risk-Based Alerting (RBA)**, and analyst triage inside Splunk (including coordination with **ReliaQuest** where applicable).

**POC scope:** On-prem **ES Dev** search head only. No separate UEBA servers. No production changes.

**Initial detection focus:** Windows authentication behavior (unusual device access, domain, and error patterns). Additional use cases (e.g. RDP-specific, data exfiltration) are out of scope unless Dev data and schedule allow.

---

## Mutual Activity Plan

| Phase | Activity | Splunk owner | Horizon owner | Target date |
|-------|----------|--------------|---------------|-------------|
| **1. Align** | Kickoff — confirm goals, stakeholders, and success criteria | Jordan / Fred | Anne / Laurence | |
| | Document top insider-threat scenarios and Exabeam pain points to compare against | Fred | Greg / Jonathan / Gary | |
| | Confirm ReliaQuest / MSSP triage workflow expectations | Jordan | Anne / Laurence | |
| **2. Platform** | Upgrade ES Dev to **8.5** (or agreed minimum) | Fred (support) | Anne / Fernando | |
| | Validate search-head capacity for UEBA workloads | Fred | Anne / Fernando | |
| **3. Data** | Confirm **Authentication** CIM data and Asset & Identity enrichment in Dev | Fred | Laurence | |
| | Run agreed validation searches; close parsing gaps | Fred | Laurence | |
| **4. Install** | Provide VOC access; install UEBA apps + content on ES Dev search head | Nerayo / Fred | Anne | |
| | Complete UEBA configuration checklist | Fred | Laurence | |
| **5. Baseline** | **~30-day warm-up** — allow models to learn normal behavior | Fred (monitor) | Anne / Laurence | |
| | Biweekly working sessions during baseline and validation | Fred | Anne / Laurence | |
| **6. Validate** | Review findings, tune exclusions; validate RBA risk scoring | Fred | Gary / Laurence | |
| | Analyst walkthrough: UEBA → ES investigation (vs Exabeam today) | Fred | Gary | |
| **7. Close** | POC readout and go / no-go recommendation | Trent / Jordan | Greg Barnes | |

**Cadence:** Biweekly working session during install, baseline, and validation phases.

---

## Success Criteria

| Use case | Success criteria | Yes / No | Date |
|----------|------------------|----------|------|
| **Confirm UEBA deployment and integration with Splunk Enterprise Security** | UEBA is operational on the **ES Dev search head** with no separate UEBA infrastructure | | |
| | UEBA detections are enabled and visible in ES Content Management | | |
| | Configuration checklist complete — no blocking install errors | | |
| **Confirm data prerequisites** | **Authentication** datamodel is populated with Windows logon data in Dev | | |
| | Asset & Identity enrichment resolves users and devices for reviewed findings | | |
| **Allow UEBA to learn normal user and entity behavior** | **~30-day baseline period** completed before findings are judged | | |
| | Baselines appear reasonable for Dev auth patterns (Horizon team confirms) | | |
| | False positives during warm-up are tunable without breaking true positives | | |
| **Identify or validate real-world risk scenarios** | UEBA produces **behavioral findings** (e.g. unusual device access, domain, or auth errors) | | |
| | Findings flow into **ES risk scores (RBA)** with actionable context | | |
| | At least **one priority insider-threat scenario** Horizon cares about is demonstrated or mapped to a finding | | |
| **Assess usability of UEBA dashboards and investigation tools** | Analysts can triage a UEBA finding in **ES without Exabeam** | | |
| | Workflow supports **ReliaQuest / MSSP handoff** (or gap is documented) | | |
| | Time to understand *who / what / why risky* is **equal to or better than** current process | | |
| **Measure alert volume and false positive rates** | Alert noise is **reduced vs duplicative Exabeam + ES correlation** for comparable scenarios (team documents comparison) | | |
| | Sampled findings are **actionable** — analysts agree a majority warrant review (target agreed at kickoff) | | |

---

## POC decision

Horizon and Splunk agree the criteria above are met → recommend evaluation of **ES Premier / UEBA for production** ahead of the **October 2026** renewal discussion.

---

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Splunk AE | Trent Singleton | | |
| Splunk SE | Jordan Codrey | | |
| Splunk SA | Fred McGhee | | |
| Horizon — Splunk admin | Anne Sun | | |
| Horizon — Splunk KM | Laurence Klose | | |
| Horizon — Security leadership | Greg Barnes | | |

---

*Technical data prerequisites (CIM fields, validation searches, ES/CMP versions) are documented separately in the Splunk team's data readiness note.*

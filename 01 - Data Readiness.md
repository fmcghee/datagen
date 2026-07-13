---
title: "01 - Data Readiness"
tags:
  - splunk/es
  - splunk/demo
  - lab201
labs: "1-3"
duration: 5 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[Demo Flow Overview]]"
next: "[[02 - Assets and Identities]]"
---

# §1 — Data Readiness

> [!note] Pre-demo / optional live
> Use as health check before customer joins, or brief "we validated your data first" moment.
> Labs 1–3 · [[Data Sources Reference]]

## Customer message

> Data must be in the right indexes with CIM allowlists applied before detections and dashboards work reliably.

## Steps

### Step 1: Confirm indexes

See [[SPL Reference#Index inventory]]

### Step 2: Validate CIM / Endpoint data model

See [[SPL Reference#Endpoint data model]]

**Knowledge check:** Which indexes should be on the Endpoint CIM allowlist?

1. **Configure → All Configurations → Data → CIM**
2. Select **Endpoint** data model
3. Set **indexes allowlist** to lab-appropriate indexes
4. Save

### Step 3: Data model acceleration

1. **Analytics → Audit → Data Model Audit** — review Acceleration Details
2. Disable acceleration on unused models (e.g., Certificates) to save compute
3. **Settings → Data Models** → Edit → uncheck Accelerate for empty models

### Check your work

See [[SPL Reference#Certificates acceleration off]]

---

← [[Demo Flow Overview]] · [[ES POV Customer Demo Guide]] · [[02 - Assets and Identities]] →

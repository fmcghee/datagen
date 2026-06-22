# ServiceNow + Splunk ES Mission Control Demo Talk Track

**Duration:** 25–30 minutes  
**Audience:** Security operations, IT leadership, Splunk ES evaluators  
**App:** `demo_servicenow_es`  
**Default time range:** Last 30 days

---

## Demo storyline

> A regional financial institution runs dual SOC queues (SOC 1 and SOC 2). Splunk
> Enterprise Security Mission Control surfaces findings from detections. Analysts
> triage in Mission Control and track remediation in ServiceNow. Splunk ties both
> together so leadership sees one operational picture.

All data is synthetic. No production ServiceNow or customer PII is used.

---

## Pre-demo checklist (15 minutes before)

| Step | Action | Validate |
|------|--------|----------|
| 1 | Install / update `demo_servicenow_es` app | App visible in Splunk |
| 2 | Confirm indexes `demo_servicenow`, `demo_security` | Index manager |
| 3 | Load scripted inputs once (disable after) | Demo Setup dashboard |
| 4 | Mission Control alerts or detections enabled & fired | `index=notable` has MC rows |
| 5 | Set browser tabs: Demo Setup, Talk Track, SOC Case Management, Mission Control Simulator, ES Mission Control | Ready to switch |
| 6 | Set time range **Last 30 days** on all dashboards | KPIs non-zero |

Validation SPL:

```spl
index=demo_servicenow sourcetype=demo:snow:incident | stats count
index=demo_security sourcetype=demo:es:incident | stats count by soc_queue
index=notable | search rule_name="*Mission Control*" OR rule_name="*SOC*" | stats count
```

---

## Act 1 — Opening (2 min)

**Screen:** Demo Talk Track (this app) or slide

**Say:**

> "Today I'll show how Splunk Enterprise Security Mission Control and ServiceNow
> work together for case management. We detect suspicious activity in ES, triage
> findings in Mission Control, and track remediation in ServiceNow — with Splunk
> linking the two so analysts don't swivel-chair between tools."

**Key message:** Detect → Triage → Remediate → Report, in one workflow.

---

## Act 2 — Data architecture (3 min)

**Screen:** Demo Setup dashboard

**Say:**

> "This demo uses a portable Splunk app with synthetic ServiceNow incidents, CMDB
> assets, and ES/Mission Control source events. Everything lands in dedicated demo
> indexes so we don't touch production data."

**Walk through indexes:**

| Index | Sourcetype | Represents |
|-------|------------|------------|
| `demo_servicenow` | `demo:snow:incident` | ServiceNow INC records |
| `demo_security` | `demo:es:incident` | ES/Mission Control source rows |
| `notable` | (ES findings) | Native Mission Control findings |

**Say:**

> "In production, ServiceNow data typically arrives via the Splunk Add-on for
> ServiceNow or API integration. ES detections write findings to Mission Control.
> Our demo simulates both sides and shows the linkage."

**Optional SPL** (Search app):

```spl
index IN (demo_servicenow, demo_security) OR index=notable
| stats count by index sourcetype
| sort index
```

---

## Act 3 — Mission Control analyst queue (8 min)

**Screen:** Enterprise Security → Mission Control → Analyst queue  
**Time range:** Last 30 days

**Say:**

> "Analysts start their day in Mission Control. Findings from correlation searches
> and detections appear here for triage, assignment, and investigation."

**Show saved views (create before demo if not done):**

- SOC 1: `"soc_queue=\"SOC 1 Queue\""`
- SOC 2: `"soc_queue=\"SOC 2 Queue\""`

**Say:**

> "We split workload across SOC 1 and SOC 2 queues. Each finding ties back to a
> ServiceNow incident number and a notable ID so we know exactly which ITSM ticket
> owns remediation."

**Open one finding — highlight fields:**

- Title (includes INC number, e.g. `INC0010001 - ...`)
- Urgency / Severity
- Owner / Status
- Entity / risk object (affected CI)
- Custom fields if configured: `snow_incident_number`, `soc_queue`

**Say:**

> "When an analyst picks up a finding, they can see the affected asset, the
> detection that fired, and the linked ServiceNow case. That context drives faster
> triage."

**Fallback:** If native Mission Control is sparse, open **Mission Control Simulator**
in this app and say:

> "This simulator reads the same source events that feed our detections — same
> queue structure, same INC linkage — useful when we're in a sandbox without full
> ES content deployed."

---

## Act 4 — ServiceNow case queue (7 min)

**Screen:** SOC Case Management dashboard (this app)

**Say:**

> "While Mission Control is the analyst's triage console, ServiceNow remains the
> system of record for ITSM. This dashboard shows the ServiceNow-side case queue."

**KPI row — narrate each:**

| KPI | Talk track |
|-----|------------|
| Open Cases | Active INCs not yet closed |
| MC Findings | Findings created in Mission Control from our demo detections |
| Linked INCs | Distinct ServiceNow cases tied to ES source events |
| High/Critical Open | Priority workload for leadership |
| Avg Open Age | Queue health metric |

**Panel: Open SOC Queue**

> "Here are open ServiceNow incidents — priority, assignee, affected CI, business
> service, and age. Click an INC number to drill into the full record."

**Drilldown:** Click an INC → show Search results with full incident fields.

**Highlight fields:**

- `u_splunk_notable_event_id` — links to ES
- `u_splunk_correlation_search` — which detection fired
- `u_mitre_tactic` / `u_mitre_technique` — framework mapping
- `cmdb_ci`, `business_service` — business impact

**Say:**

> "ServiceNow holds workflow state — New, In Progress, Resolved. Splunk enriches
> each ticket with detection context so SOC and IT ops speak the same language."

---

## Act 5 — Cross-platform linkage (6 min)

**Screen:** SOC Case Management → **Mission Control Findings Linked to ServiceNow INCs**

**Say:**

> "This is the centerpiece — one table showing how Mission Control findings,
> ES source events, and ServiceNow INCs connect."

**Walk one row:**

| Column | Meaning |
|--------|---------|
| `soc_queue` | SOC 1 or SOC 2 assignment |
| `service_now_inc` | ServiceNow ticket (INC0010001) |
| `notable_id` | ES notable identifier |
| `mc_finding_title` | Finding title in Mission Control |
| `detection_name` | Rule that created the finding |
| `inc_state` | ServiceNow workflow state |
| `linkage` | `Mission Control + ServiceNow` = fully linked |

**Say:**

> "When linkage shows 'Mission Control + ServiceNow', analysts trust that triage
> in ES and remediation in ServiceNow refer to the same incident. No manual
> copy-paste of ticket numbers."

**Panel: Mission Control Notable Events (index=notable)**

> "These are the native findings Mission Control created when our alerts fired."

**Panel: SOC Queue pie chart**

> "Workload is balanced across SOC 1 and SOC 2 for operational coverage."

---

## Act 6 — Charts & operational metrics (3 min)

**Panels:** Daily Case Trend, Case Queue by Workflow State, Assets with Case Activity

**Say:**

> "Leadership cares about trends, not just individual tickets. Daily volume shows
> whether the queue is growing. Workflow state shows if cases stall in 'On Hold'.
> Asset-centric view shows which CIs and business services drive the most case
> activity — useful for prioritizing hardening."

**Drilldown:** Click a CMDB CI → all related INCs.

---

## Act 7 — Close & value summary (2 min)

**Say:**

> "To summarize: Splunk ES Mission Control gives analysts a unified queue for
> detection triage. ServiceNow remains the ITSM system of record. Splunk links
> both with shared notable IDs, INC numbers, MITRE context, and asset metadata —
> so detect, triage, and remediate happen as one workflow instead of three tools."

**Call to action (adjust for audience):**

- **SOC:** Saved Mission Control views per queue; auto-create INC from findings
- **IT Ops:** ServiceNow dashboard driven by Splunk correlation searches
- **Leadership:** KPI dashboard for open critical cases and mean time to triage

---

## Q&A — common questions

**Q: Is this real ServiceNow data?**  
A: No. All records are synthetic, generated for demo purposes.

**Q: How would this connect to our ServiceNow?**  
A: Typically via Splunk Add-on for ServiceNow (incidents, CMDB, changes) plus ES
detections writing findings to Mission Control.

**Q: Why two SOC queues?**  
A: Models tier-1/tier-2 or regional split. Filter on `soc_queue` in Mission Control.

**Q: What if Mission Control findings don't appear?**  
A: Enable classic ES scheduled alerts with Finding/Notable action (same SPL as the
detection templates). Use Mission Control Simulator in this app as fallback. See
`docs/MISSION_CONTROL_ALTERNATIVES.md`.

**Q: Can we refresh dates before a customer demo?**  
A: Yes — rebuild the app package with rolling timestamps and reload scripted inputs.

---

## Optional Dashboard Studio import

For a richer layout, import `docs/soc_case_management_dashboard_studio.json` into
Dashboard Studio (see Demo Setup dashboard).

---

## Demo flow quick reference

```
1. Talk Track (context)
2. Demo Setup (architecture) — optional
3. ES Mission Control (native findings)
4. SOC Case Management (ServiceNow + linkage)
5. Mission Control Simulator (fallback / SOC queue filter)
6. Q&A
```

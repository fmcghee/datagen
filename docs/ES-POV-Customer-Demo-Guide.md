# Splunk Enterprise Security — Customer Demo Guide

**Purpose:** Step-by-step demo script distilled from the ES POV Lab 201 training lab for customer-facing proof-of-value sessions.

**Audience:** Solution Architects, Sales Engineers, and SOC demo presenters.

**Recommended demo length:** 45–60 minutes (core flow) or 90 minutes (with optional deep dives).

---

## Important note on source material

The original lab guide lives on Cisco SharePoint:

`ES POV Lab 201 Final Lab Guide.docx`

This document could not be read directly from that SharePoint link in the build environment (authentication required). The steps below are compiled from:

- Standard ES POV Lab 201 demo flows (detection → investigation → threat intel → automation)
- Splunk ES 8 Mission Control and SOAR integration patterns
- The `datagen` repo in this workspace for synthetic ServiceNow and security telemetry

**If you have the original `.docx`, upload it to this repo and we can align this guide line-for-line with the official lab.**

---

## What you are demonstrating

| Capability | Customer value | Where to show it |
| --- | --- | --- |
| Unified TDIR platform | One console for detect, investigate, respond | ES home, Mission Control |
| Detections / correlation searches | Proactive alerting from normalized data | Incident Review or Analyst Queue |
| Threat intelligence | Faster triage with IOC context | Threat Intelligence, Intelligence tab |
| Risk-based prioritization | Focus on what matters most | Asset priority, urgency scoring |
| Investigations | Structured case management | Mission Control investigations |
| SOAR automation | Reduce manual toil, consistent response | Automation tab, Run Playbook |
| ITSM enrichment | Bridge security and operations | ServiceNow demo data (this repo) |

---

## Before the demo

### 1. Environment checklist

- [ ] Splunk Enterprise Security installed and licensed
- [ ] Demo security telemetry indexed (auth, endpoint, DNS, network, web)
- [ ] CIM-compliant sourcetypes and tags in place
- [ ] Correlation searches enabled and generating findings/notables
- [ ] Threat intelligence sources configured (native and/or TIM Cloud)
- [ ] Splunk SOAR paired with ES (for automation section)
- [ ] At least one SOAR playbook available (e.g., Threat Intel Investigate)
- [ ] Pop-up blocker disabled for the demo URL
- [ ] Browser cache cleared or use incognito mode

### 2. Demo accounts (lab defaults — change for production)

| Role | Username | Password | Use for |
| --- | --- | --- | --- |
| Admin | `admin` | per environment | Configuration sections |
| Analyst | `analyst` or `soc_analyst` | per environment | Investigation workflow |

### 3. Load demo data (this repo)

If you are using the synthetic datasets in this repository:

**Security telemetry (HEC):**

```bash
export SPLUNK_HEC_URL="https://http-inputs-<stack>.splunkcloud.com/services/collector/event"
export SPLUNK_HEC_TOKEN="<your-hec-token>"

# Dry-run first
python3 send_csv_to_splunk.py --dry-run

# Send data
python3 send_csv_to_splunk.py
```

**ServiceNow-style data:**

Copy or symlink ServiceNow CSVs into `output/` with the names expected by `send_csv_to_splunk.py`, or ingest JSONL directly per `datasets/servicenow/README.md`.

**Validate ingestion:**

```spl
index IN (demo_security, demo_servicenow)
| stats count earliest(_time) as earliest latest(_time) as latest by index sourcetype
| convert ctime(earliest) ctime(latest)
| sort index sourcetype
```

### 4. Suggested demo storyline

Use one coherent narrative across all sections:

> An analyst notices elevated critical findings. Investigation reveals activity tied to expired identities and suspicious external IPs. Threat intelligence confirms known-bad indicators. The analyst opens an investigation, enriches with context, runs a SOAR playbook, and documents resolution — optionally creating a ServiceNow incident for IT operations.

---

## Demo flow overview

```text
1. Open ES & Security Posture          (5 min)
2. Triage a finding                    (8 min)
3. Show detection / correlation        (7 min)
4. Threat intelligence enrichment      (8 min)
5. Risk-based prioritization           (5 min)
6. Build / extend an investigation     (10 min)
7. Run SOAR playbook from ES           (10 min)
8. ServiceNow / ITSM tie-in (optional) (5 min)
9. Wrap-up & next steps                (2 min)
```

---

## Section 1 — Open ES and show Security Posture (5 min)

**Talking point:** ES turns high-volume log data into actionable security signals.

### Steps

1. Log in to Splunk Web.
2. Open **Enterprise Security** from the app list.
3. On the ES home page, point out:
   - Security Posture
   - Incident Review / Mission Control
   - App Configuration
4. Go to **Security Posture**.
5. Review **Key Indicators** — totals and 24-hour change.
6. Walk through the four panels:
   - Notable Events by Urgency
   - Notable Events Over Time
   - Top Notable Events
   - Top Notable Event Sources
7. Click the **Critical** bar in Notable Events by Urgency.
   - This drills into high-priority items (opens Incident Review or filtered queue).
8. Return to Security Posture.
9. In **Top Notable Events**, click a high-volume correlation search (e.g., expired user identity or threat intel match).
   - Show that ES filters directly to that detection type.

### Customer message

> "Your analysts do not search billions of raw events. ES surfaces the small set that needs human attention."

---

## Section 2 — Triage a finding in Mission Control / Incident Review (8 min)

**Talking point:** Structured triage reduces alert fatigue and creates an audit trail.

> **ES 8+:** Use **Mission Control → Analyst Queue**.  
> **Earlier ES:** Use **Incident Review**.

### Steps

1. Open **Mission Control** (or **Incident Review**).
2. Set time range to **Last 24 hours**.
3. Filter to a compelling scenario:
   - Search for a suspicious username (lab example: `Hax0r`)
   - Or filter by correlation search: `Activity from Expired User Identity`
   - Or filter by security domain: `Endpoint`
4. Open one finding / notable event.
5. Show:
   - **Contributing events** (raw evidence)
   - **Drill-down search** (pre-built context)
   - Urgency, severity, security domain
6. Assign and update status:
   - Select finding(s) → **Assign to me**
   - Set status to **In Progress**
7. Show queue management:
   - Filter **Status = New** to see unassigned work
   - Filter **Owner = me** to see personal queue
8. Resolve one item as a teaching example:
   - Status → **Resolved**
   - Comment: e.g., `Firewall rule updated; expired account disabled`

### Optional: Adaptive Response (no SOAR required)

1. On a notable with a `dest` host, open **Actions → Run Adaptive Response Actions**.
2. Add **Ping** action:
   - Host field: `dest`
   - Max results: `4`
3. Run and show result in Adaptive Responses list.

### Customer message

> "Every action is tracked. New analysts follow the same workflow as senior analysts."

---

## Section 3 — Detections and correlation searches (7 min)

**Talking point:** Detections turn patterns in CIM-normalized data into findings.

### Steps

1. Go to **Configure → Content → Content Management**.
2. Filter **Type = Correlation Search**.
3. Open a built-in search relevant to your storyline, for example:
   - `Activity from Expired User Identity`
   - `Threat - Threat Intelligence Match - Rule`
   - `Brute Force Access Behavior Detected`
4. Show the SPL and explain:
   - Data model / index source
   - Filter (`where`) conditions
   - Threshold (`stats`, `where count > N`)
   - Adaptive response / notable action
5. Show throttling / grouping (if configured):
   - "No more than one notable per host every 5 minutes"
6. Return to **Incident Review / Analyst Queue**.
7. Confirm findings from that search are appearing.

### Optional: Create a simple custom detection (guided mode)

Use only if time allows and you are on `admin`:

1. **Configure → Content → Content Management → Create New Content → Correlation Search**
2. Guided mode example — prohibited SSH login:
   - Data model: `Authentication` → `Successful_Authentication`
   - Filter: `app = sshd`
   - Notable title: `Successful SSH connection on host $host$`
   - Severity: High
   - Security domain: Access
3. Save, wait 2–5 minutes, then validate:

```spl
index=notable search_name="*SSH*"
| table _time search_name severity src dest host
| sort - _time
```

### Customer message

> "You can start with Splunk content and tune it to your environment — or build net-new detections without leaving the ES UI."

---

## Section 4 — Threat intelligence (8 min)

**Talking point:** Intelligence enrichment answers "Have we seen this before?" and "How bad is it?"

### Part A — Review existing intelligence

1. Go to **Configure → Data Enrichment → Intelligence Downloads** (native TI).
   - Or **Configure → Threat Intelligence** / TIM Cloud sources (ES 8+).
2. Show active feeds (e.g., Talos, public blocklists).
3. Go to **Security Intelligence → Threat Intelligence → Threat Artifacts**.
4. Filter by an intel source ID.
5. Open the **Network** tab → **IP Intelligence** panel.
6. Show matched IPs, descriptions, and weights.

### Part B — Show intelligence on a finding

1. Return to **Mission Control / Incident Review**.
2. Open a **Threat Intelligence Match** finding.
3. Show observables (IP, domain, file hash).
4. On ES 8 with TIM Cloud: open the **Intelligence** tab inside the investigation.
5. Explain weight and risk contribution.

### Part C — Add a supplemental threat list (admin demo)

1. **Configure → Data Enrichment → Intelligence Downloads → New**
2. Example values:
   - Name: `hijacked_ip_addresses`
   - Type: `hijacks`
   - URL: your approved threat feed URL
   - Delimiter: `:`
   - Fields: `description:$1,ip:$2`
3. Save and confirm it appears in the list.
4. Validate in Threat Artifacts after download completes.

### Validation SPL

```spl
index=notable search_name="*Threat Intelligence*"
| stats count by src dest threat_match_value threat_collection
| sort - count
```

### Customer message

> "Threat intel is not a separate portal — it is embedded in the analyst workflow at triage time."

---

## Section 5 — Risk-based prioritization with assets (5 min)

**Talking point:** Not all alerts are equal. Asset context changes urgency.

### Steps

1. In **Incident Review / Analyst Queue**, find endpoint findings for a test asset (lab pattern: `PROD-MFS-*`).
2. Note current **Urgency** (often Medium when asset priority is Low).
3. Go to **Configure → Data Enrichment → Asset and Identity Management**.
4. Open the asset lookup (e.g., `assets.csv` or `simple_asset_lookup`).
5. Find the demo hosts and change **priority** from `low` to `critical`.
6. Save and wait 2–3 minutes.
7. Return to the queue and refresh the same search.
8. Show urgency is now **Critical**.

### Customer message

> "A malware detection on a PCI database is not the same as one on a QA laptop. ES reflects that automatically."

---

## Section 6 — Investigations (10 min)

**Talking point:** Investigations preserve context across people, tools, and time.

### Steps

1. In **Incident Review / Analyst Queue**, filter to your storyline correlation search.
2. Select multiple related findings.
3. Click **Add Selected to Investigation → Create Investigation**.
4. Name it (e.g., `Expired Account Activity — Demo`).
5. Set status **In Progress** and save.
6. Open the investigation.
7. Walk through:
   - **Artifacts** (users, hosts, IPs)
   - **Explore** on selected artifacts (endpoint, network, identity data)
   - **Notes** — add an analyst note
   - **Timeline** of events
8. Enable **Related Notable Event Livefeed** (bell icon):
   - Toggle notifications for new related findings
9. Optional: add a custom workbench tab/panel if your environment has one configured.

### Customer message

> "Handoffs between shifts and tiers do not lose context. Everything lives in one investigation record."

---

## Section 7 — SOAR playbooks from ES (10 min)

**Talking point:** Automate enrichment and response without leaving the SIEM.

**Prerequisite:** ES paired with Splunk SOAR (Cloud or on-prem).

### Option A — Run playbook from Analyst Queue (fastest for demos)

1. Open **Mission Control → Analyst Queue**.
2. Select a finding or investigation.
3. Click **Run playbook**.
4. Choose a playbook, for example:
   - **Threat Intel Investigate** — enriches indicators and prompts for tagging
   - **Internal Host WinRM Investigate** — endpoint collection (if connector configured)
5. Click **Run playbook**.
6. Open the finding/investigation details.
7. In **Automation history**, show:
   - Playbook status
   - Action outputs
   - Analyst prompts (if any)

### Option B — Run playbook from inside an investigation

1. Open an investigation from the Analyst Queue.
2. Select the **Automation** tab.
3. Click **Run playbook** or **Run Action**.
4. Select app/action (e.g., VirusTotal, ServiceNow, firewall connector).
5. Execute and review results in Automation history.

### Option C — Show automation rules (admin / architecture audiences)

1. In Splunk SOAR, open **Automation Rules** (or ES dispatch configuration).
2. Show how a specific detection can auto-trigger a playbook.
3. Explain analyst visibility and override controls.

### Suggested narration while playbook runs

> "While the analyst reviews the investigation, SOAR is enriching indicators, querying threat feeds, and optionally opening tickets — in parallel, from one click."

### Customer message

> "Tier-1 analysts get Tier-3 enrichment automatically. Your team scales without linear headcount growth."

---

## Section 8 — ServiceNow / ITSM integration (optional, 5 min)

**Talking point:** Security and IT operations share one record of truth.

This repo includes synthetic ServiceNow data linked to Splunk notables via `u_splunk_notable_event_id`.

### Load demo ServiceNow data

```bash
# Copy ServiceNow CSVs to output/ with expected names, then:
python3 send_csv_to_splunk.py
```

Or ingest JSONL per `datasets/servicenow/README.md`.

### Demo SPL — incidents linked to ES notables

```spl
index=demo_servicenow sourcetype=demo:snow:incident u_splunk_notable_event_id=*
| table _time number priority severity status dest business_service u_splunk_notable_event_id u_splunk_correlation_search
| sort - _time
```

### Demo SPL — risk context from CMDB

```spl
index=demo_servicenow sourcetype=demo:snow:cmdb_ci (u_pci_scope=true OR u_contains_pii=true)
| table dest dest_ip business_service environment u_criticality u_edr_status owner
```

### Show in the demo

1. Open a security incident with `u_splunk_notable_event_id` populated.
2. Show CMDB fields: `u_pci_scope`, `u_criticality`, `business_service`.
3. Explain bidirectional flow:
   - ES finding → ServiceNow incident (SOAR playbook)
   - CMDB context → ES urgency / prioritization

---

## Section 9 — Wrap-up talking points (2 min)

Close with outcomes, not features:

1. **Detect** — Correlation searches on CIM data with MITRE-aligned content.
2. **Enrich** — Threat intelligence and asset/identity context at triage.
3. **Investigate** — Mission Control investigations with full audit trail.
4. **Respond** — SOAR playbooks and adaptive actions from the same console.
5. **Operate** — ITSM integration for handoff to IT and change management.

### Suggested next steps for the customer

- Identify 3–5 high-priority use cases (phishing, identity, endpoint, cloud, fraud)
- Map data sources to CIM models
- Run a 2–4 week POV with their own data
- Define success metrics: MTTD, MTTR, analyst hours saved, coverage gaps closed

---

## Quick-reference validation searches

```spl
# All notables in last 24h
index=notable earliest=-24h
| stats count by search_name severity urgency
| sort - count

# Threat intel matches
index=notable search_name="*Threat Intelligence*"
| table _time src dest user threat_match_value

# Risk modifiers
| `get_risk_correlation`
| stats sum(risk_score) as total_risk by risk_object risk_object_type
| sort - total_risk

# Security telemetry by sourcetype
index=demo_security
| stats count by sourcetype
```

---

## Troubleshooting during live demos

| Issue | Quick fix |
| --- | --- |
| No findings in queue | Widen time range; confirm correlation searches enabled |
| Playbook button missing | Verify ES–SOAR pairing and user permissions |
| Threat intel empty | Check Intelligence Downloads / TIM Cloud source status |
| Low urgency on important assets | Update asset lookup priority; wait 2–3 min |
| Pop-up blocked for drill-down | Disable pop-up blocker for demo host |
| Search timeout | Narrow time range; use `tstats` / accelerated data models |

---

## Appendix — Map to ES POV Lab 201 modules

Use this table to cross-reference the original training lab when you have access to the SharePoint document:

| Demo section | Typical POV lab topic |
| --- | --- |
| Section 1 | ES overview, Security Posture dashboard |
| Section 2 | Incident Review / Mission Control triage |
| Section 3 | Correlation searches, detection builder |
| Section 4 | Threat Intelligence Framework / TIM Cloud |
| Section 5 | Asset and Identity Framework, risk scoring |
| Section 6 | Investigations, workbench, livefeed |
| Section 7 | SOAR playbooks, adaptive response, automation rules |
| Section 8 | ITSM / ServiceNow integration |

---

## Document history

| Version | Date | Notes |
| --- | --- | --- |
| 1.0 | 2026-07-12 | Initial customer demo guide compiled from ES POV Lab patterns and datagen repo |

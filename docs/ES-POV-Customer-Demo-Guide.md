# Splunk Enterprise Security — Customer Demo Guide

**Source:** ES POV Lab 201 Final Lab Guide (201 Level)  
**Purpose:** Customer-facing proof-of-value demo script distilled from the SA training lab  
**Audience:** Solution Architects, Sales Engineers, SOC demo presenters  
**Demo customer:** OmniSphere Credit (fictional regional bank — use as your narrative anchor)

**Recommended length:** 60 minutes (core story) · 90 minutes (with threat intel + UEBA deep dives)

**Obsidian vault:** `obsidian/ES-POV-Customer-Demo/` — linked notes with YAML frontmatter. Start at `ES POV Customer Demo Guide.md`.

---

## Customer story: OmniSphere Credit

| Attribute | Detail |
| --- | --- |
| Industry | Financial Services — regional bank, ~$8B assets |
| Size | 3,500 employees, 120 branches |
| SOC | 12-person SOC, 2-tier model, 1 content engineer |
| Current state | Splunk Enterprise for 3 years; evaluating **ES Premier Cloud** |
| Adversary focus | **Scattered Spider** — phishing (T1566), persistence (T1543.003), privilege escalation (TA0004) |

### Pain points to reference in the demo

- Analysts drowning in Sentinel alerts with **no risk prioritization**
- Manual phishing triage (~45 min per alert), inconsistent process
- No formal threat intel program; feeds used ad hoc
- Insider risk concerns — privileged users accessing customer data
- Recent audit findings on triage time and incident documentation

### Technical success criteria (your demo must hit these)

| # | Success criterion | Demo section |
| --- | --- | --- |
| 1 | Data ingested, normalized, available in ES dashboards, data models, and detections | §1 Data readiness |
| 2 | Anomalous user behavior (insider risk) → separate queue for insider threat team | §6 UEBA |
| 3 | End-to-end investigation with triage and enrichment in ES | §7 Incident management |
| 4 | EDR alerts → intermediate findings in risk index | §3 Detection engineering |
| 5 | User-reported email auto-analyzed; only malicious stay in email queue | §8 Automated threat analysis |
| 6a | Asset and identity enrichment on findings | §2 Assets & identities |
| 6b | IOC enrichment (URLs, domains, hashes, IPs) via threat feeds | §4–5 Threat intelligence |

---

## Included lab data sources

Reference this table when explaining coverage to the customer.

| Description | Index | Sourcetype |
| --- | --- | --- |
| Windows Security | `win` | `XmlWinEventLog:Security` |
| Windows PowerShell | `win` | `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational` |
| Windows Sysmon | `win` | `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` |
| Windows System / Application | `win` | `WinEventLog:System`, `WinEventLog:Application` |
| Active Directory | `win` | `XmlWinEventLog:Directory Service` |
| Okta Identity Cloud | `main` | `OktaIM2:log` |
| CrowdStrike Device | `main` | `crowdstrike:device:json` |
| Cisco Secure Endpoint | `cisco` | `cisco:se` |
| AWS Metadata (BOTSv4) | `botsv4` | `aws:metadata` |
| Tenable Assets | `main` | `tenable:io:assets` |

---

## Demo flow at a glance

```text
OPENING     OmniSphere story + success criteria           (3 min)
§1          Data exploration & CIM readiness              (5 min)  [pre-demo / optional]
§2          Exposure Analytics — assets & identities      (8 min)
§3          Detection engineering & risk index            (10 min)
§4          Threat Intelligence (TIM Cloud)               (10 min)
§5          Threat object enrichment on findings          (8 min)
§6          UEBA — insider threat queue                   (8 min)
§7          Mission Control — queues, investigations, RP  (10 min)
§8          Automated email threat analysis               (8 min)
CLOSE       Outcomes recap + POV next steps                 (3 min)
```

---

## Opening (3 min)

**Say this:**

> "OmniSphere Credit is a regional bank evaluating ES Premier after struggling with alert noise in their current SIEM. Their CISO wants faster phishing triage, formal threat intel, insider risk visibility, and documented investigations. Today we'll walk through how ES addresses each of those — using their hybrid environment and the Scattered Spider TTPs they're most worried about."

Show the success criteria table above and tell the customer which items you'll demonstrate live vs. what was pre-staged in the POV environment.

---

## §1 — Data exploration & readiness (5 min)

*Use as a pre-demo health check or a brief "we validated your data first" moment.*

### Step 1: Confirm indexes

```spl
| eventcount summarize=false index=*
| dedup index
| fields index
```

### Step 2: Validate CIM / Endpoint data model

```spl
| tstats count from datamodel=Endpoint by sourcetype index
```

**Customer message:** Data must be in the right indexes with CIM allowlists applied before detections and dashboards work reliably.

### Step 3: Confirm data model acceleration

- Navigate to **Analytics → Audit → Data Model Audit**
- Confirm acceleration is on for models you use (Endpoint, Authentication, etc.)
- Disable acceleration on empty models (e.g., Certificates) to save compute

### Check your work

```spl
| rest splunk_server=local count=0 /services/data/models
| search title=Certificates
| table title acceleration
```

---

## §2 — Assets, identities & Exposure Analytics (8 min)

**Talking point:** Findings are only useful when you know *who* and *what* is at risk.

### Demo steps

1. **Configure → Exposure Analytics → Start setup** (if not already done).
2. Show **Entity discovery sources** — Okta, AWS EC2, AD, Linux SSHD, etc.
3. Explain OmniSphere's identity migration story: static identity list with title-based priority:
   - Director/VP/C-level → **Critical**
   - Manager/Supervisor/Lead → **Medium**
   - Engineer/Developer/Analyst → **High**
   - Sales/HR → **Low**
4. Show enrichment rule example — map `user_country` to `user_region` (North America vs Europe after bank acquisition).
5. Validate identity lookup:

```spl
| inputlookup identity_lookup_expanded
| search identity=ghoppy AND category=employee
| table identity priority bunit category email
```

6. Tie to findings: show how asset/identity context changes urgency on Mission Control findings.

### Customer message

> "Exposure Analytics continuously discovers users and assets from your existing logs — no separate CMDB project required to get started. Business context like executive priority and region flows into risk scoring automatically."

---

## §3 — Detection engineering & risk index (10 min)

**Talking point:** OmniSphere's biggest pain is noise. ES uses **risk-based alerting** — many detections feed the risk index first; high cumulative risk creates findings.

### Detection lifecycle (30-second framing)

1. Define objectives (Scattered Spider TTPs)
2. Identify data requirements
3. Implement, test, validate
4. Continuous tuning
5. Report metrics (MTTD, coverage, false positive rate)

### Demo steps — Scattered Spider risk stack

Show these detections enabled with **risk index output only** (not standalone findings):

| Detection | MITRE | Risk fields |
| --- | --- | --- |
| Detect Mimikatz With PowerShell Script Block Logging | T1003.001 | dest, user_id |
| Malicious PowerShell Process With Obfuscation Techniques | T1059.001 | dest |
| Windows File Download Via PowerShell | T1105 | dest, user |
| Registry Keys Used For Persistence | T1547.001 | dest, user |
| FodHelper UAC Bypass | T1548.002 | dest, user |
| TeamViewer on endpoint (risk index only) | — | per detection |

**Show in UI:**

1. **Security content → Content management** — filter enabled detections.
2. Explain macro tuning (e.g., `index=win` in PowerShell macro for performance).
3. Show tuned noisy detections (Windows Group Discovery, System Information Discovery) outputting **intermediate findings** with low risk scores.
4. **Highlight custom detection:** Cisco Secure Endpoint process creation → risk index with severity-based scores (Low=20, Medium=30, High=40, Critical=50).

### Validate risk accumulation

```spl
index=risk earliest=-24h
| stats sum(risk_score) as total_risk by risk_object risk_object_type source
| sort - total_risk
| head 10
```

### Customer message

> "Instead of 500 equal-priority alerts, your analysts see risk accumulating on users and systems. A single low-fidelity signal might be ignored; the same host with five signals becomes a finding worth investigating."

---

## §4 — Threat Intelligence: TIM Cloud (10 min)

**Talking point:** OmniSphere has no formal CTI program. TIM Cloud operationalizes intel inside Mission Control.

### TIM vs TIF — when to explain

| Scenario | Recommendation |
| --- | --- |
| Small SOC, enrichment only | **TIM only** |
| Detection + enrichment, some custom feeds | **TIF + TIM** |
| ES + SOAR with advanced enrichment | **TIF + TIM + SOAR TI integrations** |
| Just starting, keep it simple | **TIM first** with open-source feeds |

**Key difference for customers:**

- **TIF (ES Native):** IOC matching in log data → generates findings/intermediate findings
- **TIM (Cloud):** Curated, scored indicators → enriches observables on the **Intelligence tab** in investigations

### Demo steps — TIM Cloud sources

1. **Configure → Threat Intelligence → Data Sources**
2. Show activated feeds (examples from lab):
   - Cisco SMA — Indicators & Analysis feeds
   - Abuse SSL IP Blacklist (open source)
   - DHS-AIS (industry CERT)
   - AlienVault OTX (customer's own API key)
3. Filter by **Status = Activated** — all green.

### Demo steps — Threatlists & safelists

1. **Configure → Threat Intelligence → Threatlists → Add**
2. Name the threatlist, select up to 10 TIM sources, enable all indicator types.
3. Set threatlist **Active**.
4. Show **Safelists** — default excludes `localhost`; bulk-add known-good items (Google DNS, internal RFC1918 ranges) to reduce false enrichment.

### Customer message

> "Your analysts don't paste hashes into VirusTotal. When a finding fires, TIM enriches observables automatically — domain reputation, file analysis, certificate metadata — right in the investigation."

---

## §5 — Threat object enrichment on findings (8 min)

**Talking point:** Enrichment only works when detections extract the right observables.

### Demo scenario 1 — File hash from process events

1. Open detection **ESCU - Dump LSASS via procdump – Rule**.
2. Explain: `process_name` is a weak IOC; **file_hash (SHA256)** is reliable.
3. Show added SPL extracting hashes from multi-value `process_hash` field:

```spl
| rex field=process_hash max_match=0 "MD5=(?<md5>[^,]+).+SHA256=(?<sha256>[^,]+).+IMPHASH=(?<imphash>[^,]+)"
| eval file_hash = sha256
```

4. Show threat object mapping: `file_hash` → type `file_hash`.

### Demo scenario 2 — URL from command line

1. Open **ESCU - BITSAdmin Download File - Rule**.
2. Show URL extraction:

```spl
| rex field=process "(?<url>https?://[^\s\"]+)"
```

3. Add threat object: `url` → type `url`.

### Demo scenario 3 — Cisco Talos adaptive response

1. **Mission Control** → find a BITSAdmin Download File finding.
2. **Actions → Run Adaptive Response → Intelligence Enrichment with Talos**
3. Select observable type **URL**, run action.
4. Show Talos results added to finding notes.

### Customer message

> "We tune detections to emit the observables your threat feeds can act on — hashes, URLs, IPs — so enrichment is automatic, not a manual analyst step."

---

## §6 — UEBA & insider threat queue (8 min)

**Talking point:** OmniSphere needs a **separate queue** for insider risk — not mixed with external threat findings.

### Demo steps

1. **Analytics → UEBA** — show Top Risky Users (e.g., **JDavis**).
2. Click user → **Findings tab** → detection heatmap.
3. Explain UEBA detections run to `ba_test` first, then **Turn on in risk index** for production.
4. Show risk output:

```spl
index=risk earliest=-24h source="UEBA*"
| stats count by source risk_object
| sort - count
```

5. Show tuning — entity list + finding exclusion for accepted benign behavior (e.g., JDavis PowerShell pattern).
6. Return to UEBA dashboard — excluded detection removed from user's heatmap.
7. Navigate to **Insider Threat** team queue (configured in §7) — show watchlist-based routing.

### Customer message

> "External attackers and insider risk are different workflows. UEBA behavioral detections route to a dedicated insider threat queue so your IR team isn't buried in credential-stuffing noise."

---

## §7 — Incident management: queues, investigations, response plans (10 min)

**Talking point:** OmniSphere's audit found poor incident documentation. Mission Control fixes that.

### Step 1 — Team queues (Lab 17)

Show two pre-configured queues:

| Queue | Route condition | Purpose |
| --- | --- | --- |
| **User-reported Email Analysis** | `incident_origin = IMAP v2 – buttercup-security` | Phishing triage |
| **Insider Threat** | `watchlist = true` | Insider risk findings |

**Demo:**

1. **Configure → Findings and investigations → Team queues**
2. Show queue conditions, roles (`ess_analyst`), 7-day retention.
3. Open **User-reported Email Analysis** queue.
4. Show custom table view **Finding Triage** with threat analysis fields.
5. Filter: `threat analysis status = completed`.

### Step 2 — Investigation types (Lab 18)

1. **Configure → Findings and investigations → Investigation types**
2. Show types: `email`, `insider_threat`
3. Explain custom fields and response plan association per type.

### Step 3 — Response plans (Lab 19)

1. **Security content → Response plans**
2. Show **Workflow Email Phishing Response** plan (AI-imported from SOP).
3. Show plan assigned to `email` investigation type.
4. Start an investigation on an email finding → walk through response plan tasks.

### Step 4 — End-to-end investigation workflow

1. **Mission Control → Analyst Queue** — select a finding.
2. **Assign to me** → status **In Progress**.
3. **Start investigation** — review events, observables, Intelligence tab.
4. Add note, run adaptive response or playbook.
5. Update status through resolution.

### Customer message

> "Every investigation has a type, a response plan, and a team queue. Your SOC runs the same phishing playbook every time — and leadership can audit it."

---

## §8 — Automated threat analysis (email) (8 min)

**Talking point:** Cut phishing triage from 45 minutes to minutes with automated analysis in the analyst queue.

### How it works

- **Third-party findings** ingest SOAR app events directly as ES findings.
- **Automated Threat Analysis** (ES 8.5+) uses SAA engines (email, web, static analysis) for verdict and score.
- Only emails deemed malicious remain in the email queue after analysis completes.

### Demo steps (Lab 20)

1. **Configure → Splunk SOAR → Apps** — filter **Support ES ingestion**.
2. Show **IMAP v2** app configured with `buttercup-security` asset (lab-provided; do not share credentials in customer docs).
3. Explain ingest settings:
   - Investigation type: `email`
   - Security domain: network
   - Urgency: medium
4. **Poll Now** (max 5 objects) — findings appear in **User-reported Email Analysis** queue.
5. Click finding → review **threat analysis** in side panel (verdict, score).
6. **Start Investigation → View complete analysis** — full SAA forensics.

### Validate

```spl
index=notable search_name="Manual Finding Event - Rule"
| stats count
```

### Customer message

> "Analysts used to spend 45 minutes per reported phish. Now the platform analyzes the email automatically — your team only investigates what SAA flags as malicious."

---

## Closing — outcomes & POV next steps (3 min)

Recap against OmniSphere success criteria:

| Criterion | Demonstrated |
| --- | --- |
| Data optimization | CIM models, lab data sources indexed |
| Anomaly / insider detection | UEBA → Insider Threat queue |
| Incident management | Investigation + response plan + documentation |
| EDR → risk index | Cisco Secure Endpoint custom detection |
| Email triage automation | IMAP ingest + Automated Threat Analysis |
| Asset/identity enrichment | Exposure Analytics |
| Threat intel enrichment | TIM Cloud + threat objects + Talos |

### Suggested POV next steps for the customer

1. Map OmniSphere's top 5 data sources to CIM (use their CrowdStrike, Okta, Cisco SE, Windows logs).
2. Enable Scattered Spider-aligned detections with risk index first; tune for 2 weeks before promoting to findings.
3. Activate TIM Cloud with customer's OTX/API keys; build one threatlist.
4. Stand up two team queues matching their SOC structure (email + insider or cloud + endpoint).
5. Import one response plan from their existing phishing SOP.
6. Define POV success metrics: MTTD, phishing triage time, % findings with TI enrichment, analyst hours saved.

---

## Appendix A — Pre-demo technical checklist (SA only)

Run these before the customer joins:

- [ ] CIM allowlists set for Endpoint (and other used models)
- [ ] Data model acceleration verified
- [ ] Exposure Analytics entity sources enabled
- [ ] Risk-index detections enabled (Scattered Spider stack)
- [ ] Cisco Secure Endpoint detection + field aliases configured
- [ ] TIM Cloud sources activated; threatlist active
- [ ] Threat object fields on LSASS + BITSAdmin detections
- [ ] UEBA detections on in risk index
- [ ] Team queues: Email Analysis + Insider Threat
- [ ] Investigation types + email response plan published
- [ ] IMAP v2 polled; email findings in queue
- [ ] Pop-up blocker disabled

### Enabled detection count check

```spl
| rest splunk_server=local count=0 /servicesNS/-/-/saved/searches
| where match('action.correlationsearch.enabled', "1|[Tt]|[Tt][Rr][Uu][Ee]")
| where disabled=0
| stats count
```

*Lab expects 14+ enabled detections when fully configured.*

---

## Appendix B — Optional deep dives (not in 60-min core demo)

| Topic | Lab reference | When to use |
| --- | --- | --- |
| Custom TIF TAXII feeds | Labs 14–15, cabby/curl optional | Mature CTI team, custom feed requirements |
| TIF + TIM dual configuration | Configuring Custom Sources | Customer needs IOC matching *and* enrichment |
| Detection tuning / exclusions | Labs 10–11 | Technical deep-dive with content engineer |
| Static identity CSV import | Lab 5 | Customer with identity migration story |
| ServiceNow integration | `datasets/servicenow/` in this repo | ITSM handoff story |

### ServiceNow demo data (this repo)

```bash
python3 send_csv_to_splunk.py   # after copying SNOW CSVs to output/
```

```spl
index=demo_servicenow sourcetype=demo:snow:incident u_splunk_notable_event_id=*
| table _time number priority severity status u_splunk_notable_event_id u_splunk_correlation_search
```

---

## Appendix C — Map to official lab modules

| Official lab | Customer demo section |
| --- | --- |
| Labs 1–3: Data exploration | §1 |
| Labs 4–7: Exposure Analytics | §2 |
| Labs 8–11: Detection engineering | §3 |
| Labs 12–14: TIM Cloud | §4 |
| Lab 14 enrichment + Lab 15 Talos | §5 |
| Lab 16: UEBA | §6 |
| Labs 17–19: Queues, investigation types, response plans | §7 |
| Lab 20: IMAP / automated threat analysis | §8 |

---

## Document history

| Version | Date | Notes |
| --- | --- | --- |
| 1.0 | 2026-07-12 | Initial guide from ES POV patterns + datagen repo |
| 2.0 | 2026-07-12 | Aligned to ES POV Lab 201 Final Lab Guide PDF; OmniSphere Credit storyline |

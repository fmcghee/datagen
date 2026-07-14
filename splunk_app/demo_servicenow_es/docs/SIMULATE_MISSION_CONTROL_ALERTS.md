# Simulate Mission Control Alerts (ES 8.5)

Native **Mission Control** shows findings created by Enterprise Security **Notable / Finding**
alert actions writing to `index=notable`. Demo source rows in `demo:es:incident` alone are not
enough — you must enable the bundled scheduled alerts below.

## Prerequisites

1. Indexes: `demo_servicenow`, `demo_security`
2. Run **Load Demo Data → LOAD ALL DEMO DATA** (or `demo_load_all_data`)
3. Confirm source rows:

```spl
index=demo_security sourcetype=demo:es:incident | stats count by soc_queue
```

## Enable bundled alerts (fastest)

1. Open **ServiceNow ES Demo → Simulate Mission Control Alerts**
2. Go to **Settings → Searches, reports, and alerts**
3. Filter app: `demo_servicenow_es`
4. Open each alert and click **Enable**:
   - `demo_mc_alert_soc1`
   - `demo_mc_alert_soc2`
5. Wait 5 minutes (or **Edit → Run** if your role allows)
6. Validate:

```spl
index=notable earliest=-90d
| search rule_name="Demo - Mission Control SOC*"
| stats count by rule_name
```

7. Open **Enterprise Security → Mission Control → Analyst queue** (Last 90 days)

### Mission Control saved views

```text
"soc_queue=\"SOC 1 Queue\""
"soc_queue=\"SOC 2 Queue\""
```

## Manual setup (if bundled alerts need UI fix)

Create alerts from **Enterprise Security** (not Search & Reporting):

### SOC 1 alert

**Name:** `Demo - Mission Control SOC 1 Queue Linked INC - Rule`

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
| table _time name description snow_incident_number notable_id soc_queue urgency severity assignee risk_object risk_score cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

| Setting | Value |
|---------|--------|
| Trigger | Number of results **> 0**, **For each result** |
| Schedule | Every 5 minutes |
| Time range | Last 90 days |
| Action | **Notable** or **Finding** |

| Notable field | Token |
|---------------|--------|
| Title | `$name$` |
| Description | `$description$` |
| Security domain | `threat` |
| Severity | `$severity$` |
| Entity type | `system` |
| Entity | `$risk_object$` |
| Suppress on | `$notable_id$` for 7 days |

Repeat for SOC 2 with `soc_queue="SOC 2 Queue"`.

## ES 8.5 event-based detection (alternative)

Copy SPL from `demo_es85_detection_soc1_template` / `demo_es85_detection_soc2_template`
into **Security content → Event-based detection** with **Output → Create findings**.

If detections do not write to `index=notable` on your stack, use classic alerts above.

## What does NOT work

- `| makeresults` alone
- `| collect index=notable` without Notable/Finding action
- Mission Control Simulator (dashboard-only, not native MC queue)

## Disable after demo

Disable `demo_mc_alert_soc1` and `demo_mc_alert_soc2` to stop new findings.

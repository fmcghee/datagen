# Mission Control / ES incident source data

This directory contains synthetic Splunk Enterprise Security incident source
events that are linked to generated ServiceNow `INC` records.

## Files

| File | Purpose |
| --- | --- |
| `csv/es_incidents.csv` | CSV source rows for ES correlation searches |
| `jsonl/es_incidents.jsonl` | JSONL copy of the same rows |
| `../../output/es_incidents.csv` | HEC-ready CSV used by `send_csv_to_splunk.py` |

Each row includes fields commonly useful in Mission Control and ES demos:

- `snow_incident_number` / `service_now_incident`
- `notable_id`
- `soc_queue`
- `queue`
- `status_name`
- `urgency`
- `assignee`
- `risk_object`
- `cmdb_ci`
- `business_service`
- `correlation_search`

The generated `soc_queue` values are:

- `SOC 1 Queue`
- `SOC 2 Queue`

## Important Mission Control note

Sending `es_incidents.csv` to HEC creates searchable source events. It does not
by itself create findings in the Mission Control analyst queue. Use Enterprise
Security detections to create **findings** from these source rows.

### ES 8.5 vs older ES / standalone Mission Control

| Deployment | What you configure | "Mission Control Incidents" adaptive response |
| --- | --- | --- |
| **ES 8.5** (Mission Control built into ES) | Event-based detection → **Output: Create findings** | **Not available and not needed** |
| **ES 7.x + standalone Splunk Mission Control app** | Correlation search → Notable + Mission Control Incidents | Required (or auto-added every 15 min) |

If you are on **ES 8.5** and do not see **Mission Control Incidents** in the
adaptive response list, that is expected. Findings created by detections appear
directly on **Mission Control → Analyst queue** without a separate adaptive
response action.

## UI-only workflow (ES 8.5)

### 1. Ingest the source data

From the machine where this repo is available:

```bash
python3 scripts/generate_servicenow_demo_data.py --base-time now
python3 scripts/validate_mission_control_demo.py
python3 send_csv_to_splunk.py --output-dir output
```

This sends `output/es_incidents.csv` to:

```text
index=demo_security sourcetype=demo:es:incident
```

Validate in Splunk Search:

```spl
index=demo_security sourcetype=demo:es:incident
| stats count values(snow_incident_number) as linked_INC values(notable_id) as notable_ids by soc_queue status_name urgency
```

### 2. Create event-based detections (ES 8.5)

In Splunk Enterprise Security:

1. Select **Security content** → **Content management**.
2. Select **+ Content** → **Detection** → **Event-based detection**.
3. Create one detection per SOC queue (or one detection for both queues and
   filter later in saved views).

#### SOC 1 detection

**Name:** `Demo - Mission Control SOC 1 Queue Linked INC - Rule`

**Search:**

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
| table _time name description snow_incident_number service_now_incident notable_id soc_queue status_name urgency severity assignee owner risk_object cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

#### SOC 2 detection

**Name:** `Demo - Mission Control SOC 2 Queue Linked INC - Rule`

**Search:**

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 2 Queue"
| table _time name description snow_incident_number service_now_incident notable_id soc_queue status_name urgency severity assignee owner risk_object cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

#### Analyst queue output (this replaces Notable + Mission Control Incidents)

For each detection, in the detection editor:

1. Open **Analyst queue information**.
2. Under **Output**, select **Create findings** (do not rely on a separate
   Mission Control adaptive response action).
3. Configure:

   | Field | Value |
   | --- | --- |
   | Finding name | `$name$` |
   | Description | `$description$` |
   | Entity | `$risk_object$` |
   | Investigation type | Any enabled type (for example Default) |
   | Severity | Map from `$severity$` or set manually (critical/high) |
   | Default owner | `$assignee$` (optional) |
   | Default status | New |

4. Under **Conditions**, set **Create when** to match your demo (for example
   **Number of results** ≥ 1) and trigger **For each result** so each ingested
   row becomes its own finding.
5. Set a schedule (for example every 5–15 minutes) or run once after ingest.
6. **Save** and **Enable** the detection.

The `| table ...` step is required so custom fields such as `soc_queue` and
`snow_incident_number` are carried into each finding.

#### Optional: show custom fields on finding details

1. Select **Configure** → **Findings and investigations** (or **Incident
   Management** → finding field settings, depending on your ES build).
2. **Add field** for each demo field you want visible, for example:

   | Label | Field |
   | --- | --- |
   | SOC Queue | `soc_queue` |
   | ServiceNow INC | `snow_incident_number` |
   | Notable ID | `notable_id` |
   | CMDB CI | `cmdb_ci` |
   | Business Service | `business_service` |

3. Select **Save** at the bottom of the page.

You do **not** need to add **Mission Control Incidents** as an adaptive response
action on ES 8.5. That action belongs to the standalone Splunk Mission Control
app used with ES 7.x Cloud integrations.

### 3. Create SOC 1 and SOC 2 saved views in Mission Control

1. Open **Mission Control** → **Analyst queue**.
2. Use the search/filter bar. ES 8.5 requires the filter SPL to be wrapped in
   double quotes:

   SOC 1 saved view:

   ```text
   "soc_queue=\"SOC 1 Queue\""
   ```

   SOC 2 saved view:

   ```text
   "soc_queue=\"SOC 2 Queue\""
   ```

3. Save each filter as a shared or personal saved view.

### 4. Demo validation (ES 8.5)

Indexed source rows:

```spl
index=demo_security sourcetype=demo:es:incident
| table _time name snow_incident_number notable_id soc_queue status_name urgency assignee risk_object cmdb_ci business_service
| sort soc_queue - _time
```

Findings in the notable index (Mission Control analyst queue source):

```spl
index=notable rule_name="Demo - Mission Control SOC*"
| table _time rule_name title snow_incident_number notable_id soc_queue urgency owner risk_object
| sort soc_queue - _time
```

Validate from the **Mission Control → Analyst queue** UI using the saved views
above. You should see 9 findings per queue after the detections run.

---

## Legacy workflow (ES 7.x + standalone Splunk Mission Control)

Use this only if your deployment still uses correlation searches and the
standalone Splunk Mission Control app.

### Create correlation searches

Same SPL as the ES 8.5 detections above, but create them under **Configure** →
**Content** → **Content management** as correlation searches.

For each correlation search:

1. Enable the **Notable** adaptive response action (`$name$`, `$description$`).
2. Add the **Mission Control Incidents** adaptive response action (or wait up
   to 15 minutes for the modular input to attach it automatically).

### Mission Control saved views

Same quoted filters as the ES 8.5 section. If `| mcincidents` is available:

```spl
| mcincidents
| search soc_queue="SOC 1 Queue" OR soc_queue="SOC 2 Queue"
| table create_time id name status_name urgency assignee soc_queue snow_incident_number risk_object
```


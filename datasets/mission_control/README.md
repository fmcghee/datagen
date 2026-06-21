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
by itself create native Mission Control incidents. To make these appear in
Mission Control, use Enterprise Security to create Notable events from these
source rows and enable the Mission Control incident action.

## UI-only workflow

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

### 2. Create ES correlation searches in the Splunk UI

Create two correlation searches in Splunk Enterprise Security.

#### SOC 1 correlation search

Search:

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
| table _time name description snow_incident_number service_now_incident notable_id soc_queue status_name urgency severity assignee risk_object cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

Suggested title:

```text
Demo - Mission Control SOC 1 Queue Linked INC
```

#### SOC 2 correlation search

Search:

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 2 Queue"
| table _time name description snow_incident_number service_now_incident notable_id soc_queue status_name urgency severity assignee risk_object cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

Suggested title:

```text
Demo - Mission Control SOC 2 Queue Linked INC
```

For each correlation search:

1. Enable the **Notable** adaptive response action.
2. Set the notable title/name to include the INC, for example:

   ```text
   $name$
   ```

3. Set the description to:

   ```text
   $description$
   ```

4. Map severity/urgency from the event if your ES UI allows field tokens, for
   example `$severity$` or `$urgency$`.
5. Add or confirm the **Mission Control Incidents** adaptive response action.
   In many ES/Mission Control deployments, Mission Control automatically creates
   incidents from ES notables; adding the action makes that behavior explicit.

### 3. Create SOC 1 and SOC 2 queue views in Mission Control

In Mission Control / Analyst Queue, create saved filtered views:

SOC 1 Queue filter:

```spl
soc_queue="SOC 1 Queue"
```

SOC 2 Queue filter:

```spl
soc_queue="SOC 2 Queue"
```

If your Mission Control UI requires quoted SPL filters, use:

```text
"soc_queue=\"SOC 1 Queue\""
```

and:

```text
"soc_queue=\"SOC 2 Queue\""
```

### 4. Demo validation

Search indexed source rows:

```spl
index=demo_security sourcetype=demo:es:incident
| table _time name snow_incident_number notable_id soc_queue status_name urgency assignee risk_object cmdb_ci business_service
| sort soc_queue - _time
```

Search Mission Control incident data, where available:

```spl
| mcincidents
| search soc_queue="SOC 1 Queue" OR soc_queue="SOC 2 Queue"
| table create_time id name status_name urgency assignee soc_queue snow_incident_number risk_object
```

If `mcincidents` is not available in your deployment, use the Mission Control
Analyst Queue filters above and validate from the UI.


# datagen

Synthetic demo data generators and ready-to-use datasets.

## Available datasets

- [`datasets/servicenow`](datasets/servicenow/README.md) - realistic synthetic
  ServiceNow incident, change, user, CMDB, and task-CI data for Splunk Enterprise
  Security demos.

## Send CSV demo data to Splunk Cloud with HEC

Use `send_csv_to_splunk.py` to read CSV files from the `output/` directory and
send each row to Splunk HTTP Event Collector (HEC) as a JSON event. CSV columns
are preserved inside the JSON event payload so Splunk can extract them as event
fields.

### Refresh current-dated demo data

Regenerate the ServiceNow demo data before a customer demo so timestamps roll
forward with the current UTC calendar:

```bash
python3 scripts/generate_servicenow_demo_data.py --base-time now
python3 scripts/validate_servicenow_cim.py
```

This writes the canonical ServiceNow dataset under `datasets/servicenow/` and
HEC-ready CSV aliases under `output/`:

```text
output/servicenow_incidents.csv
output/servicenow_cmdb.csv
output/servicenow_changes.csv
output/servicenow_users.csv
```

For a fully repeatable static dataset, use:

```bash
python3 scripts/generate_servicenow_demo_data.py --static
```

### Supported CSV files

| CSV file in `output/` | Splunk index | Splunk sourcetype |
| --- | --- | --- |
| `auth.csv` | `demo_security` | `demo:auth` |
| `endpoint.csv` | `demo_security` | `demo:endpoint` |
| `dns.csv` | `demo_security` | `demo:dns` |
| `network.csv` | `demo_security` | `demo:network` |
| `web.csv` | `demo_security` | `demo:web` |
| `servicenow_incidents.csv` | `demo_servicenow` | `demo:snow:incident` |
| `servicenow_cmdb.csv` | `demo_servicenow` | `demo:snow:cmdb_ci` |
| `servicenow_changes.csv` | `demo_servicenow` | `demo:snow:change` |
| `servicenow_users.csv` | `demo_servicenow` | `demo:snow:user` |
| `es_incidents.csv` | `demo_security` | `demo:es:incident` |

The script parses the first available timestamp field from `_time`, `time`,
`timestamp`, or `opened_at` and sends it as the Splunk HEC event `time`. The
original CSV timestamp field remains in the JSON event.

### Splunk Cloud setup

1. In Splunk Cloud, create or confirm the target indexes:
   - `demo_security`
   - `demo_servicenow`
2. Enable or create an HTTP Event Collector token with permission to write to
   those indexes.
3. Confirm your HEC endpoint. Splunk Cloud HEC URLs usually look like:

   ```text
   https://http-inputs-<stack>.splunkcloud.com/services/collector/event
   ```

4. Export the HEC URL and token in your shell. Do not commit these values.

   ```bash
   export SPLUNK_HEC_URL="https://http-inputs-<stack>.splunkcloud.com/services/collector/event"
   export SPLUNK_HEC_TOKEN="<your-hec-token>"
   ```

### Run

Dry-run first to validate CSV headers, timestamp parsing, and file mapping
without sending data:

```bash
python3 send_csv_to_splunk.py --dry-run
```

If only the ServiceNow demo files are present in `output/`, the dry-run prints
warnings for missing security telemetry CSVs. That is expected unless you have
also generated `auth.csv`, `endpoint.csv`, `dns.csv`, `network.csv`, and
`web.csv`.

Send all supported CSV files that exist in `output/`:

```bash
python3 send_csv_to_splunk.py
```

Fail if any expected CSV is missing:

```bash
python3 send_csv_to_splunk.py --require-all
```

Use a different CSV output directory:

```bash
python3 send_csv_to_splunk.py --output-dir /path/to/output
```

### Validation SPL

Confirm data arrived by index and sourcetype:

```spl
index IN (demo_security, demo_servicenow)
| stats count earliest(_time) as earliest latest(_time) as latest by index sourcetype
| convert ctime(earliest) ctime(latest)
| sort index sourcetype
```

Validate ServiceNow incident fields:

```spl
index=demo_servicenow sourcetype=demo:snow:incident
| table _time number priority severity status assignment_group cmdb_ci business_service u_splunk_notable_event_id
| sort - _time
```

Validate CMDB fields:

```spl
index=demo_servicenow sourcetype=demo:snow:cmdb_ci
| table _time name dest dest_ip ip mac nt_host owner business_service u_criticality
```

Validate security telemetry sourcetypes:

```spl
index=demo_security sourcetype IN (demo:auth, demo:endpoint, demo:dns, demo:network, demo:web)
| stats count by sourcetype
```

Validate ES incident source rows that can feed Mission Control:

```spl
index=demo_security sourcetype=demo:es:incident
| stats count values(snow_incident_number) as linked_servicenow_cases by soc_queue status_name urgency
```

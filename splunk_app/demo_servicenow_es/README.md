# ServiceNow ES Demo Splunk App

Portable Splunk app for ServiceNow + Enterprise Security + Mission Control demos.

## What is included

- Bundled synthetic CSV demo data under `bin/data/`
- Scripted inputs to index demo data without HEC
- CIM-friendly sourcetype, eventtype, and tag configuration
- SOC case-management dashboard
- Demo setup dashboard with install instructions
- Saved searches for validation and ES 8.5 detection templates

## Quick install

1. Build or refresh bundled data from the repository root:

   ```bash
   python3 scripts/build_splunk_demo_app.py --package
   ```

2. Copy `splunk_app/demo_servicenow_es` or install `dist/demo_servicenow_es.tar.gz`
   to `$SPLUNK_HOME/etc/apps/` on your search head.

3. Restart Splunk.

4. Open the **ServiceNow ES Demo** app and follow the **Demo Setup** dashboard.

## Indexes

Create these indexes before loading data:

- `demo_servicenow`
- `demo_security`

See `default/indexes.conf.example`.

## Load demo data

Enable each scripted input under **Settings > Data inputs > Scripts** once, then
disable it again to prevent duplicate events. Marker files in `local/` track
which CSV files were already loaded.

## ES 8.5 Mission Control

Use the saved searches `demo_es85_detection_soc1_template` and
`demo_es85_detection_soc2_template` as SPL templates for event-based detections
with **Output > Create findings**. Mission Control Incidents adaptive response
is not required on ES 8.5.

If detections cannot create native findings on your stack, use **Mission Control
Simulator** in this app instead. It reads `demo:es:incident` rows and presents
SOC 1 / SOC 2 queue views for demos. See
`datasets/mission_control/ALTERNATIVES.md` for other fallback methods.

## HEC alternative

You can still use the repository script `send_csv_to_splunk.py` if you prefer
HEC ingestion instead of scripted inputs.

## Refresh demo dates

```bash
python3 scripts/build_splunk_demo_app.py --package
```

Reinstall the refreshed app, delete `local/loaded_*.marker`, and reload inputs
with `--force` if needed.

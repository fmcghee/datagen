# ServiceNow ES Demo Splunk App

Portable Splunk app for ServiceNow + Enterprise Security + Mission Control demos.

## What is included

- Bundled synthetic CSV demo data under `bin/data/`
- Scripted inputs to index demo data without HEC
- CIM-friendly sourcetype, eventtype, and tag configuration
- **Demo Talk Track** — in-app 25–30 minute presenter script (`DEMO_TALK_TRACK.md` + dashboard)
- **SOC Case Management** dashboard with Mission Control ↔ ServiceNow linkage
- **Mission Control Simulator** fallback when native findings are unavailable
- Demo setup dashboard with install instructions
- Saved searches for validation, MC linkage, and ES 8.5 detection templates
- Dashboard Studio JSON and Mission Control alternatives under `docs/`

## Quick install

1. Build or refresh bundled data from the repository root:

   ```bash
   python3 scripts/build_splunk_demo_app.py --package
   ```

2. Copy `splunk_app/demo_servicenow_es` or install `dist/demo_servicenow_es.tar.gz`
   to `$SPLUNK_HOME/etc/apps/` on your search head.

3. Restart Splunk.

4. Open the **ServiceNow ES Demo** app and follow the **Demo Setup** dashboard.

## Demo flow

1. **Demo Setup** — install, load data, configure Mission Control
2. **Demo Talk Track** — presenter script (Acts 1–7)
3. **SOC Case Management** — ServiceNow queue + MC linkage KPIs and tables
4. **Mission Control Simulator** — fallback analyst queue by SOC 1 / SOC 2

Set time range to **Last 30 days** on all dashboards.

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

**Primary path:** event-based detections with **Output > Create findings**, or
classic ES scheduled alerts with a **Finding / Notable** action. Both populate
`index=notable` and the Mission Control analyst queue.

Use the saved searches `demo_es85_detection_soc1_template` and
`demo_es85_detection_soc2_template` as SPL templates. Mission Control Incidents
adaptive response is not required on ES 8.5.

Run `demo_validate_mc_linkage` to confirm cross-index linkage before a live demo.

If detections cannot create native findings on your stack, use **Mission Control
Simulator** in this app instead. See `docs/MISSION_CONTROL_ALTERNATIVES.md`.

## Dashboard Studio

Import `docs/soc_case_management_dashboard_studio.json` into Dashboard Studio for
a richer layout. See repository `dashboards/README.md` for import steps.

## HEC alternative

You can still use the repository script `send_csv_to_splunk.py` if you prefer
HEC ingestion instead of scripted inputs.

## Refresh demo dates

```bash
python3 scripts/build_splunk_demo_app.py --package
```

Reinstall the refreshed app, delete `local/loaded_*.marker`, and reload inputs
with `--force` if needed.

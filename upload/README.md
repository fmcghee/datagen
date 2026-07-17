# Upload these files to Splunk

Copy or download from this folder to install the demo app.

**Package built:** 2026-07-14 (rolling demo timestamps; data lands in recent time ranges)

**Includes:** Load Demo Data saved searches, SOC Case Management dashboard, Mission Control Simulator, Simulate Mission Control Alerts (`demo_mc_alert_soc1` / `demo_mc_alert_soc2`), AppInspect-clean conf (no `local/`), Splunk Cloud lookup-based data load path.

## Recommended (single file upload)

| File | Use |
|------|-----|
| **demo_servicenow_es.tar.gz** | Install via Splunk **Manage Apps → Install app from file** |

## Alternative

| File | Use |
|------|-----|
| **demo_servicenow_es_folder.tar.gz** | Same app, packaged from the app folder (extract then copy to `$SPLUNK_HOME/etc/apps/`) |

## Install steps

1. Download `demo_servicenow_es.tar.gz` from this folder (or from `dist/` in the repo).
2. In Splunk: **Apps → Manage Apps → Install app from file**.
3. Choose the `.tar.gz` file and install.
4. Restart Splunk (or reload the app).
5. Open **ServiceNow ES Demo** and go to **Demo Setup**.

## Repo paths (if browsing the codebase)

```
upload/demo_servicenow_es.tar.gz          ← use this for upload
dist/demo_servicenow_es.tar.gz            ← same file (build output)
splunk_app/demo_servicenow_es/            ← app source (folder install)
```

## Rebuild before a customer demo

From repository root:

```bash
python3 scripts/build_splunk_demo_app.py --package
cp dist/demo_servicenow_es.tar.gz upload/
```

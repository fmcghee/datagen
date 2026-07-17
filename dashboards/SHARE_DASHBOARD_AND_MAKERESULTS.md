# Dashboard creation commands and makeresults SPL

Share this page when someone needs to build the SOC dashboards or inject quick
demo rows with `| makeresults`.

---

## 1. Build command (package dashboards into the Splunk app)

From the repository root:

```bash
python3 scripts/build_splunk_demo_app.py --package
cp dist/demo_servicenow_es.tar.gz upload/
```

What this does:

- Syncs `dashboards/soc_case_management_simple_xml.xml` → app view `soc_case_management.xml`
- Syncs `dashboards/soc_case_management_dashboard_studio.json` → app `docs/soc_case_management_dashboard_studio.json`
- Refreshes bundled CSV demo data and creates `dist/demo_servicenow_es.tar.gz`

Install the app:

```bash
# Splunk UI: Apps → Manage Apps → Install app from file → demo_servicenow_es.tar.gz
# Or folder install:
cp -r splunk_app/demo_servicenow_es $SPLUNK_HOME/etc/apps/
```

After install, dashboards are available under **ServiceNow ES Demo** (Simple XML
views ship with the app). Dashboard Studio JSON is imported manually (below).

---

## 2. Dashboard Studio import (manual UI steps)

Source file: `dashboards/soc_case_management_dashboard_studio.json`

1. Splunk → **Dashboards**
2. **Create new dashboard** → choose **Dashboard Studio**
3. Open the dashboard **Source** editor
4. Replace all JSON with the contents of `soc_case_management_dashboard_studio.json`
5. **Save**
6. Set time range to **Last 365 days**

---

## 3. Classic Simple XML dashboard (manual UI steps)

Source file: `dashboards/soc_case_management_simple_xml.xml`

1. Splunk → **Dashboards**
2. **Create new dashboard** → choose **Classic Dashboard** (Simple XML)
3. **Edit** → **Source**
4. Replace all XML with the contents of `soc_case_management_simple_xml.xml`
5. **Save**
6. Set time range to **Last 365 days**

Or copy directly into an app views folder (requires app reload/restart):

```bash
cp dashboards/soc_case_management_simple_xml.xml \
  $SPLUNK_HOME/etc/apps/demo_servicenow_es/default/data/ui/views/soc_case_management.xml
```

---

## 4. makeresults SPL (shareable)

### Important limitation

`| makeresults` alone does **not** populate **native Mission Control**. Mission
Control needs ES **Notable / Finding** alert actions writing to `index=notable`.

Use makeresults for:

- Quick Search testing
- Ad-hoc dashboard panel prototyping
- Writing synthetic rows into `index=demo_security` for the **Mission Control Simulator** and **SOC Case Management** dashboards

---

### A. Search-only — one demo row (paste into Splunk Search)

```spl
| makeresults count=1
| eval _time=now()
| eval name="INC0010001 - Multiple failed VPN logins followed by success for JPatel"
| eval description="Synthetic Mission Control demo row from makeresults for dashboard testing."
| eval snow_incident_number="INC0010001"
| eval service_now_incident="INC0010001"
| eval notable_id="NE-DEMO-0001"
| eval soc_queue="SOC 1 Queue"
| eval status_name="New"
| eval urgency="critical"
| eval severity="critical"
| eval assignee="soc1_triage"
| eval owner="soc1_triage"
| eval risk_object="vpn-gw-01"
| eval risk_score=94
| eval cmdb_ci="vpn-gw-01"
| eval business_service="Corporate VPN"
| eval correlation_search="Demo - Mission Control makeresults rule"
| eval mitre_tactic="Credential Access"
| eval mitre_technique="T1110"
| table _time name description snow_incident_number notable_id soc_queue status_name urgency severity assignee risk_object risk_score cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

---

### B. Search-only — SOC 1 and SOC 2 sample rows

```spl
| makeresults count=2
| streamstats count AS row
| eval _time=now() - (row * 3600)
| eval name=case(row=1,
    "INC0010001 - Multiple failed VPN logins followed by success for JPatel",
    "INC0010002 - EDR malware quarantine on fin-lt-014")
| eval description=case(row=1,
    "SOC 1 makeresults demo row linked to INC0010001.",
    "SOC 2 makeresults demo row linked to INC0010002.")
| eval snow_incident_number=case(row=1, "INC0010001", "INC0010002")
| eval service_now_incident=snow_incident_number
| eval notable_id=case(row=1, "NE-DEMO-0001", "NE-DEMO-0002")
| eval soc_queue=case(row=1, "SOC 1 Queue", "SOC 2 Queue")
| eval status_name=case(row=1, "New", "In Progress")
| eval urgency=case(row=1, "critical", "high")
| eval severity=case(row=1, "critical", "high")
| eval assignee=case(row=1, "soc1_triage", "soc2_investigator")
| eval owner=assignee
| eval risk_object=case(row=1, "vpn-gw-01", "edr-mgmt-01")
| eval risk_score=case(row=1, 94, 60)
| eval cmdb_ci=risk_object
| eval business_service=case(row=1, "Corporate VPN", "Security Monitoring")
| eval correlation_search="Demo - Mission Control makeresults rule"
| eval mitre_tactic=case(row=1, "Credential Access", "Execution")
| eval mitre_technique=case(row=1, "T1110", "T1204")
| table _time name description snow_incident_number notable_id soc_queue status_name urgency severity assignee risk_object risk_score cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

---

### C. Index demo rows (feeds Mission Control Simulator / SOC dashboards)

Run once in Search. Requires index `demo_security` (from the demo app).

```spl
| makeresults count=2
| streamstats count AS row
| eval _time=now() - (row * 3600)
| eval name=case(row=1,
    "INC0010001 - Multiple failed VPN logins followed by success for JPatel",
    "INC0010002 - EDR malware quarantine on fin-lt-014")
| eval description=case(row=1,
    "SOC 1 makeresults demo row linked to INC0010001.",
    "SOC 2 makeresults demo row linked to INC0010002.")
| eval snow_incident_number=case(row=1, "INC0010001", "INC0010002")
| eval service_now_incident=snow_incident_number
| eval notable_id=case(row=1, "NE-DEMO-0001", "NE-DEMO-0002")
| eval soc_queue=case(row=1, "SOC 1 Queue", "SOC 2 Queue")
| eval status_name=case(row=1, "New", "In Progress")
| eval urgency=case(row=1, "critical", "high")
| eval severity=case(row=1, "critical", "high")
| eval assignee=case(row=1, "soc1_triage", "soc2_investigator")
| eval owner=assignee
| eval risk_object=case(row=1, "vpn-gw-01", "edr-mgmt-01")
| eval risk_score=case(row=1, 94, 60)
| eval cmdb_ci=risk_object
| eval business_service=case(row=1, "Corporate VPN", "Security Monitoring")
| eval correlation_search="Demo - Mission Control makeresults rule"
| eval mitre_tactic=case(row=1, "Credential Access", "Execution")
| eval mitre_technique=case(row=1, "T1110", "T1204")
| collect index=demo_security sourcetype=demo:es:incident addtime=false marker=0
```

Validate:

```spl
index=demo_security sourcetype=demo:es:incident notable_id=NE-DEMO-*
| table _time name soc_queue snow_incident_number notable_id severity
```

---

### D. Native Mission Control (makeresults is not enough)

To populate **native Mission Control**, save scheduled alerts with a **Notable /
Finding** action. Use demo source data (or makeresults output) as alert input —
do not rely on `| collect index=notable` alone.

**SOC 1 alert SPL** (from indexed demo data):

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
| table _time name description snow_incident_number notable_id soc_queue urgency severity assignee risk_object risk_score cmdb_ci business_service correlation_search mitre_tactic mitre_technique
```

Save as alert in **Enterprise Security** → trigger **For each result** → add
**Notable / Finding** action → map title `$name$`, description `$description$`,
severity `$severity$`, entity `$risk_object$`.

Full steps: `splunk_app/demo_servicenow_es/docs/SIMULATE_MISSION_CONTROL_ALERTS.md`

---

## 5. Dashboard data expectations

Panels expect these indexes/sourcetypes after demo data load:

```spl
index=demo_servicenow sourcetype=demo:snow:incident
index=demo_security sourcetype=demo:es:incident
index=notable rule_name="*Mission Control*"
```

Load bundled data: **ServiceNow ES Demo → Load Demo Data → LOAD ALL DEMO DATA**

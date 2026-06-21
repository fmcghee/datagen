# SOC Case Management dashboard

This directory contains two versions of the same SOC case-management dashboard.

## Dashboard Studio

Use `soc_case_management_dashboard_studio.json` for Dashboard Studio.

In Splunk:

1. Go to **Dashboards**.
2. Create a new **Dashboard Studio** dashboard.
3. Open the dashboard source editor.
4. Replace the generated source with the JSON from
   `soc_case_management_dashboard_studio.json`.
5. Save.

Dashboard Studio uses JSON source, not Simple XML.

## Classic Simple XML

Use `soc_case_management_simple_xml.xml` if you need a copy/importable XML
dashboard.

In Splunk:

1. Go to **Dashboards**.
2. Create a new **Classic Dashboard**.
3. Edit source.
4. Replace the source with the XML from `soc_case_management_simple_xml.xml`.
5. Save.

## Data expectations

Both dashboards expect the ServiceNow demo events in:

```spl
index=demo_servicenow sourcetype=demo:snow:incident
```


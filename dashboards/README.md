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

## Adjusting panel fit

If a Dashboard Studio panel clips titles, table columns, or descriptions, edit
the JSON `layout.structure[].position` values for that panel:

- `w` controls width
- `h` controls height
- `x` controls horizontal position
- `y` controls vertical position

For example, increase the open queue panel height:

```json
{
  "item": "viz_open_queue",
  "type": "block",
  "position": {
    "x": 30,
    "y": 375,
    "w": 1370,
    "h": 420
  }
}
```

The top header intentionally avoids showing raw color-code text in the dashboard.
The Deloitte palette remains applied in the JSON through the visualization
background and chart color options.


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

Both dashboards expect demo data in:

```spl
index=demo_servicenow sourcetype=demo:snow:incident
index=demo_security sourcetype=demo:es:incident
index=notable rule_name="*Mission Control*"
```

## Mission Control linkage panels

The updated dashboard adds panels that show how Mission Control findings tie to
ServiceNow INCs:

- **Mission Control Findings Linked to ServiceNow INCs** - joins
  `demo:es:incident` source rows, `index=notable` findings, and ServiceNow INC
  records on `notable_id` / `service_now_inc`.
- **Mission Control Notable Events** - native findings from `index=notable`.
- **Mission Control Source Events by SOC Queue** - SOC 1 / SOC 2 distribution.

The **linkage** column shows whether each row is tied across Mission Control and
ServiceNow (`Mission Control + ServiceNow`) or only one side.

## Drilldowns

The table panels include drilldowns that open a filtered Splunk Search in a new
tab:

- **Open SOC Queue** - click the `number` field to open that specific case.
- **Splunk ES Notable-Linked ServiceNow Cases** - click the `number` field to
  open that specific case.
- **Assets and Business Services with Case Activity** - click the `cmdb_ci`
  field to open all cases for that asset.

The Dashboard Studio JSON uses field-level `drilldown.customUrl` event handlers.
The Classic XML companion uses table `<drilldown>` links.

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

## KPI labels

The five KPI numbers near the top of the Dashboard Studio version are:

1. **Open Cases** - incidents where `state!="Closed"`
2. **MC Findings** - findings in `index=notable` from Mission Control demo detections
3. **Linked INCs** - distinct ServiceNow INCs in `demo:es:incident` source data
4. **High / Critical Open** - open incidents with priority `1 - Critical` or
   `2 - High`
5. **Avg Open Age** - average age, in hours, for the active case queue

The Dashboard Studio layout uses separate colored label bars above the KPI
values so the labels stay visible even when Splunk renders single-value panels
with compact title space.

## Chart panel sizing

The daily-volume and workflow-state charts are intentionally simplified:

- **Daily Case Trend - Last 7 Days** returns two fields: `Day` and `Cases`.
- **Case Queue by Workflow State** returns two fields: `State` and `Cases`.

This avoids crowded multi-series split-by charts and renders more reliably in
Dashboard Studio. Both charts are stacked as full-width panels in the JSON. If
your browser zoom or screen size still clips a chart, increase the relevant panel
`h` value:

- `viz_daily_volume`
- `viz_workflow_state`


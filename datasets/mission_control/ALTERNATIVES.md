# Mission Control demo alternatives (when ES detections fail)

Native Mission Control findings in ES 8.5 are created by the Enterprise Security
**finding / notable alert action pipeline**. Ingesting CSV rows or using
`| makeresults` alone does **not** reliably populate the Mission Control analyst
queue.

Use one of the approaches below for demos.

## Recommended: Mission Control Simulator dashboard

After loading `es_incidents.csv`, open the demo app:

**ServiceNow ES Demo → Mission Control Simulator**

This dashboard reads `index=demo_security sourcetype=demo:es:incident` and
provides SOC 1 / SOC 2 queue filters, KPIs, and drilldown to ServiceNow INCs.

It is the most reliable demo path when CMS event-based detections cannot create
findings on your stack.

## Option B: Classic scheduled alert (try before giving up on native MC)

Some stacks accept a **classic alert** with a Notable/Finding action even when
CMS detections fail.

1. Open **Enterprise Security** (not Search and Reporting).
2. Run the SOC 1 SPL (Last 30 days):

   ```spl
   index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
   | table _time name description snow_incident_number notable_id soc_queue status_name urgency severity assignee risk_object cmdb_ci business_service
   ```

3. **Save As → Alert** (from the ES app context).
4. Trigger: **For each result**.
5. Schedule: every 15 minutes; earliest time **-30d**.
6. Add alert action: **Notable Event** or **Finding** (whichever appears).
7. Map title `$name$`, description `$description$`, severity `$severity$`.
8. Enable the alert and wait one run cycle.

Validate:

```spl
index=notable earliest=-30d
| search rule_name="*SOC 1*" OR title="INC*"
| table _time rule_name title soc_queue snow_incident_number
```

Repeat for SOC 2.

## Option C: makeresults (limited — usually not enough alone)

`| makeresults` can fabricate rows, but Mission Control still needs ES to
process them through a **Finding/Notable alert action**. Example bridge SPL:

```spl
index=demo_security sourcetype=demo:es:incident soc_queue="SOC 1 Queue"
| head 1
| table name description snow_incident_number notable_id soc_queue urgency severity risk_object
```

Save that as a **scheduled alert inside ES** with a Finding/Notable action.
Do **not** use `| collect index=notable` alone — that writes index rows but
often skips the analyst queue KVStore sync in ES 8.x.

## Option D: Direct index=notable injection (advanced, often incomplete)

Writing JSON directly to `index=notable` via HEC or `collect` may show events in
Search but **not** in Mission Control UI. Only use for SPL validation, not live
triage demos.

To inspect the field names your stack uses for real findings:

```spl
index=notable earliest=-7d
| head 1
| fieldsummary
```

## Demo talking point

For customer demos when native Mission Control is blocked:

> "These SOC queue items are sourced from synthetic ES incident events linked to
> ServiceNow INCs. In production, the same fields would be promoted to Mission
> Control findings via ES detections."

Then show **Mission Control Simulator** plus the **SOC Case Management**
dashboard.

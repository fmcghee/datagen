---
title: SPL Reference
tags:
  - splunk/es
  - splunk/SPL
  - reference
parent: "[[ES POV Customer Demo Guide]]"
---

# SPL Reference

All validation searches for the ES POV demo.

## Index inventory

```spl
| eventcount summarize=false index=*
| dedup index
| fields index
```

## Endpoint data model

```spl
| tstats count from datamodel=Endpoint by sourcetype index
```

## Certificates acceleration off

```spl
| rest splunk_server=local count=0 /services/data/models
| search title=Certificates
| table title acceleration
```

## Identity lookup

```spl
| inputlookup identity_lookup_expanded
| search identity=ghoppy AND category=employee
| table identity priority bunit category email
```

## Risk accumulation

```spl
index=risk earliest=-24h
| stats sum(risk_score) as total_risk by risk_object risk_object_type source
| sort - total_risk
| head 10
```

## UEBA risk output

```spl
index=risk earliest=-24h source="UEBA*"
| stats count by source risk_object
| sort - count
```

## Email findings count

```spl
index=notable search_name="Manual Finding Event - Rule"
| stats count
```

## Enabled detection count

```spl
| rest splunk_server=local count=0 /servicesNS/-/-/saved/searches
| where match('action.correlationsearch.enabled', "1|[Tt]|[Tt][Rr][Uu][Ee]")
| where disabled=0
| stats count
```

## ServiceNow demo (datagen repo)

```spl
index=demo_servicenow sourcetype=demo:snow:incident u_splunk_notable_event_id=*
| table _time number priority severity status u_splunk_notable_event_id u_splunk_correlation_search
```

## Region enrichment rule check

```spl
| inputlookup ea_cleanrules
| search rule="region_enrichment"
```

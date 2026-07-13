---
title: Optional Deep Dives
tags:
  - splunk/es
  - splunk/appendix
parent: "[[ES POV Customer Demo Guide]]"
---

# Optional Deep Dives

Not in the 60-minute core demo. Use for technical audiences or extended POV sessions.

| Topic | Lab reference | When to use |
| --- | --- | --- |
| Custom TIF TAXII feeds | Labs 14–15, cabby/curl | Mature CTI team |
| TIF + TIM dual config | Configuring Custom Sources | IOC matching + enrichment |
| Detection tuning / exclusions | Labs 10–11 | Content engineer deep-dive |
| Static identity CSV import | Lab 5 | Identity migration story |
| ServiceNow integration | `datasets/servicenow/` | ITSM handoff |

## ServiceNow demo data

```bash
python3 send_csv_to_splunk.py   # after copying SNOW CSVs to output/
```

See [[SPL Reference#ServiceNow demo]].

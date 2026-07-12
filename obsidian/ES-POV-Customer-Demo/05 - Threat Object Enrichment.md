---
title: "05 - Threat Object Enrichment"
tags:
  - splunk/es
  - splunk/demo
  - threat-intel
labs: "14-15"
duration: 8 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[04 - Threat Intelligence TIM Cloud]]"
next: "[[06 - UEBA Insider Threat]]"
---

# §5 — Threat Object Enrichment

> [!warning] Prerequisite
> Enrichment only works when detections extract the right observables. See [[04 - Threat Intelligence TIM Cloud]].

Success criterion **6b** · Labs 14–15

## Scenario 1 — File hash (LSASS / procdump)

Detection: **ESCU - Dump LSASS via procdump – Rule**

- `process_name` = weak IOC (easily renamed)
- `file_hash` (SHA256) = reliable

```spl
| rex field=process_hash max_match=0 "MD5=(?<md5>[^,]+).+SHA256=(?<sha256>[^,]+).+IMPHASH=(?<imphash>[^,]+)"
| eval file_hash = sha256
```

Threat object: `file_hash` → type `file_hash`

## Scenario 2 — URL (BITSAdmin)

Detection: **ESCU - BITSAdmin Download File - Rule**

```spl
| rex field=process "(?<url>https?://[^\s\"]+)"
```

Threat object: `url` → type `url`

## Scenario 3 — Cisco Talos adaptive response

1. **Mission Control** → BITSAdmin Download File finding
2. **Actions → Run Adaptive Response → Intelligence Enrichment with Talos**
3. Observable type: **URL**
4. Show results in finding notes

## Customer message

> We tune detections to emit observables your feeds can act on — enrichment is automatic, not a manual analyst step.

---

← [[04 - Threat Intelligence TIM Cloud]] · [[06 - UEBA Insider Threat]] →

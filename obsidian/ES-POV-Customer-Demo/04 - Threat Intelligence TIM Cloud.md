---
title: "04 - Threat Intelligence TIM Cloud"
tags:
  - splunk/es
  - splunk/demo
  - threat-intel
  - TIM
labs: "12-13"
duration: 10 min
parent: "[[ES POV Customer Demo Guide]]"
prev: "[[03 - Detection Engineering]]"
next: "[[05 - Threat Object Enrichment]]"
---

# §4 — Threat Intelligence (TIM Cloud)

> [!tip] Talking point
> OmniSphere has no formal CTI program. TIM Cloud operationalizes intel inside Mission Control.

Success criterion **6b** · Labs 12–13

## TIM vs TIF

| Scenario | Recommendation |
| --- | --- |
| Small SOC, enrichment only | **TIM only** |
| Detection + enrichment, custom feeds | **TIF + TIM** |
| ES + SOAR advanced enrichment | **TIF + TIM + SOAR TI** |
| Just starting | **TIM first** (open-source feeds) |

| Capability | TIF (Native) | TIM (Cloud) |
| --- | --- | --- |
| Output | Findings via IOC match in logs | Enrichment on Intelligence tab |
| Storage | Local KV store | Cloud service |
| Custom feeds | STIX, CSV, custom formats | Limited TAXII/MISP/RSS |

## Demo — TIM Cloud sources

1. **Configure → Threat Intelligence → Data Sources**
2. Show activated feeds:
   - Cisco SMA — Indicators & Analysis
   - Abuse SSL IP Blacklist
   - DHS-AIS
   - AlienVault OTX (customer API key)
3. Filter **Status = Activated**

## Demo — Threatlists & safelists

1. **Threatlists → Add** — select up to 10 TIM sources
2. Enable all indicator types; set **Active**
3. **Safelists** — add known-good (Google DNS, internal RFC1918, etc.)

## Customer message

> Analysts don't paste hashes into VirusTotal. When a finding fires, TIM enriches observables automatically in the investigation.

→ Next: [[05 - Threat Object Enrichment]] for threat object tuning

---

← [[03 - Detection Engineering]] · [[05 - Threat Object Enrichment]] →

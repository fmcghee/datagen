---
title: Data Sources Reference
tags:
  - splunk/es
  - splunk/reference
parent: "[[ES POV Customer Demo Guide]]"
---

# Data Sources Reference

Lab indexes and sourcetypes for [[OmniSphere Credit - Customer Story|OmniSphere Credit]] POV environment.

| Description | Index | Sourcetype |
| --- | --- | --- |
| Windows Security | `win` | `XmlWinEventLog:Security` |
| Windows PowerShell | `win` | `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational` |
| Windows Sysmon | `win` | `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` |
| Windows System / Application | `win` | `WinEventLog:System`, `WinEventLog:Application` |
| Active Directory | `win` | `XmlWinEventLog:Directory Service` |
| Okta Identity Cloud | `main` | `OktaIM2:log` |
| CrowdStrike Device | `main` | `crowdstrike:device:json` |
| Cisco Secure Endpoint | `cisco` | `cisco:se` |
| AWS Metadata (BOTSv4) | `botsv4` | `aws:metadata` |
| Tenable Assets | `main` | `tenable:io:assets` |

See [[01 - Data Readiness]] for CIM validation SPL.

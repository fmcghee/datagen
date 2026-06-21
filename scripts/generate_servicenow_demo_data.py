#!/usr/bin/env python3
"""Generate deterministic, synthetic ServiceNow data for Splunk ES demos.

The generated records are fake but shaped like common ServiceNow tables used by
the Splunk Add-on for ServiceNow: incidents, change requests, CMDB CIs, users,
and task-to-CI relationships.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "datasets" / "servicenow"
CSV_ROOT = DATASET_ROOT / "csv"
JSONL_ROOT = DATASET_ROOT / "jsonl"
MISSION_CONTROL_ROOT = ROOT / "datasets" / "mission_control"
MISSION_CONTROL_CSV_ROOT = MISSION_CONTROL_ROOT / "csv"
MISSION_CONTROL_JSONL_ROOT = MISSION_CONTROL_ROOT / "jsonl"
OUTPUT_ROOT = ROOT / "output"

SEED = 8675309
DEFAULT_BASE_TIME = datetime(2026, 5, 27, 18, 0, 0, tzinfo=timezone.utc)
BASE_TIME = DEFAULT_BASE_TIME
SNOW_INSTANCE = "synthetic-servicenow"
SNOW_VENDOR = "ServiceNow"
SNOW_PRODUCT = "IT Service Management"
SNOW_VENDOR_PRODUCT = f"{SNOW_VENDOR} {SNOW_PRODUCT}"


COMPANIES = [
    "Northwind Financial",
    "Contoso Health",
    "Apex Manufacturing",
    "City Power Utility",
]

LOCATIONS = [
    "New York - HQ",
    "Chicago - Data Center",
    "Dallas - SOC",
    "London - Regional Office",
    "Singapore - Regional Office",
    "Remote",
]

SUPPORT_GROUPS = [
    "Security Operations",
    "Threat Response",
    "Identity and Access",
    "Network Operations",
    "Cloud Platform",
    "Windows Server",
    "Linux Platform",
    "Database Services",
    "Endpoint Engineering",
    "Application Support",
    "Service Desk",
]

BUSINESS_SERVICES = [
    "Online Banking",
    "Card Processing",
    "Customer Identity",
    "Corporate VPN",
    "Payments API",
    "Claims Portal",
    "ERP Finance",
    "Manufacturing MES",
    "Data Warehouse",
    "Email and Collaboration",
    "Security Monitoring",
]

DEPARTMENTS = [
    "Security",
    "Infrastructure",
    "Finance",
    "Claims",
    "Manufacturing",
    "Retail Operations",
    "Engineering",
    "Legal",
    "Human Resources",
    "Customer Support",
]

FIRST_NAMES = [
    "Avery",
    "Jordan",
    "Taylor",
    "Morgan",
    "Riley",
    "Casey",
    "Quinn",
    "Jamie",
    "Cameron",
    "Drew",
    "Reese",
    "Parker",
    "Sydney",
    "Harper",
    "Emerson",
    "Rowan",
    "Alex",
    "Hayden",
    "Kai",
    "Logan",
]

LAST_NAMES = [
    "Bennett",
    "Carter",
    "Diaz",
    "Evans",
    "Foster",
    "Garcia",
    "Hughes",
    "Ibrahim",
    "Jensen",
    "Kim",
    "Lewis",
    "Morris",
    "Nguyen",
    "Ortiz",
    "Patel",
    "Reed",
    "Singh",
    "Turner",
    "Vasquez",
    "Walker",
]

USER_TITLES = [
    "Security Analyst",
    "Threat Hunter",
    "Systems Engineer",
    "Network Engineer",
    "Database Administrator",
    "Cloud Engineer",
    "Service Desk Analyst",
    "Application Owner",
    "Finance Manager",
    "Claims Specialist",
    "Plant Supervisor",
    "Executive Assistant",
]

CI_CLASSES = [
    "cmdb_ci_server",
    "cmdb_ci_win_server",
    "cmdb_ci_linux_server",
    "cmdb_ci_database",
    "cmdb_ci_netgear",
    "cmdb_ci_appl",
    "cmdb_ci_computer",
    "cmdb_ci_cloud_service",
]

OS_CHOICES = [
    "Windows Server 2022",
    "Windows 11 Enterprise",
    "Ubuntu Server 22.04 LTS",
    "Red Hat Enterprise Linux 9",
    "Amazon Linux 2023",
    "Cisco IOS XE 17",
    "PostgreSQL 15",
    "Microsoft SQL Server 2022",
]


@dataclass(frozen=True)
class TaskLink:
    task_number: str
    task_sys_id: str
    table: str
    ci_name: str
    ci_sys_id: str
    relationship_type: str


def snow_time(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def json_time(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def current_base_time() -> datetime:
    """Return a stable, current UTC anchor for rolling demo data."""
    now = datetime.now(timezone.utc)
    return now.replace(minute=0, second=0, microsecond=0)


def parse_base_time(value: str) -> datetime:
    timestamp = value.strip()
    if timestamp.lower() in {"now", "current", "rolling"}:
        return current_base_time()

    if timestamp.endswith("Z"):
        timestamp = f"{timestamp[:-1]}+00:00"

    parsed = datetime.fromisoformat(timestamp)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic ServiceNow demo data.")
    parser.add_argument(
        "--base-time",
        default="now",
        help=(
            "UTC anchor for generated timestamps. Use 'now' for current demo data "
            "or an ISO timestamp such as 2026-06-20T12:00:00Z. Defaults to now."
        ),
    )
    parser.add_argument(
        "--static",
        action="store_true",
        help="Use the original fixed timestamp anchor for fully repeatable output.",
    )
    parser.add_argument(
        "--skip-output",
        action="store_true",
        help="Do not write HEC-ready CSV aliases into output/.",
    )
    return parser.parse_args()


def random_time(rng: random.Random, min_days_ago: int, max_days_ago: int) -> datetime:
    days = rng.randint(min_days_ago, max_days_ago)
    seconds = rng.randint(0, 86_399)
    return BASE_TIME - timedelta(days=days, seconds=seconds)


def sys_id(rng: random.Random) -> str:
    return f"{rng.getrandbits(128):032x}"


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict[str, str]], table: str, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            event_time = json_time(parse_snow_time(row.get("sys_updated_on") or row.get("sys_created_on"))) or row.get("_time", "")
            event = {
                **row,
                "_time": event_time,
                "table": table,
                "source": source,
            }
            handle.write(json.dumps(event, sort_keys=True) + "\n")


def parse_snow_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def priority_for(impact: str, urgency: str) -> str:
    matrix = {
        ("1 - High", "1 - High"): "1 - Critical",
        ("1 - High", "2 - Medium"): "2 - High",
        ("2 - Medium", "1 - High"): "2 - High",
        ("2 - Medium", "2 - Medium"): "3 - Moderate",
        ("1 - High", "3 - Low"): "3 - Moderate",
        ("3 - Low", "1 - High"): "3 - Moderate",
        ("2 - Medium", "3 - Low"): "4 - Low",
        ("3 - Low", "2 - Medium"): "4 - Low",
        ("3 - Low", "3 - Low"): "5 - Planning",
    }
    return matrix[(impact, urgency)]


def make_users(rng: random.Random) -> list[dict[str, str]]:
    users: list[dict[str, str]] = []
    seen: set[str] = set()

    synthetic_people = [(first, last) for first in FIRST_NAMES for last in LAST_NAMES]
    rng.shuffle(synthetic_people)

    for index, (first_name, last_name) in enumerate(synthetic_people[:64], start=1):
        base_name = f"{first_name[0]}{last_name}".lower()
        user_name = base_name
        suffix = 2
        while user_name in seen:
            user_name = f"{base_name}{suffix}"
            suffix += 1
        seen.add(user_name)

        department = rng.choice(DEPARTMENTS)
        title = rng.choice(USER_TITLES)
        manager = "" if index <= 8 else rng.choice(users[: min(len(users), 16)])["name"]
        active = "true" if rng.random() > 0.06 else "false"
        user = {
            "sys_id": sys_id(rng),
            "user_name": user_name,
            "employee_number": f"E{100000 + index}",
            "name": f"{first_name} {last_name}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{user_name}@northwind.example",
            "title": title,
            "department": department,
            "company": rng.choice(COMPANIES),
            "manager": manager,
            "location": rng.choice(LOCATIONS),
            "active": active,
            "vip": "true" if title in {"Finance Manager", "Executive Assistant"} and rng.random() < 0.2 else "false",
            "u_mfa_status": rng.choices(["Enrolled", "Pending", "Exception"], weights=[84, 11, 5])[0],
            "u_identity_provider": rng.choice(["Okta", "Entra ID", "PingFederate"]),
            "u_risk_score": str(rng.randint(1, 85)),
            "sys_created_on": snow_time(random_time(rng, 150, 720)),
            "sys_updated_on": snow_time(random_time(rng, 0, 45)),
        }
        users.append(user)

    automation_time = snow_time(BASE_TIME - timedelta(days=300))
    users.append(
        {
            "sys_id": sys_id(rng),
            "user_name": "soc_automation",
            "employee_number": "SVC1001",
            "name": "SOC Automation",
            "first_name": "SOC",
            "last_name": "Automation",
            "email": "soc_automation@northwind.example",
            "title": "Automation Integration",
            "department": "Security",
            "company": "Northwind Financial",
            "manager": "Jordan Bennett",
            "location": "Dallas - SOC",
            "active": "true",
            "vip": "false",
            "u_mfa_status": "Non-interactive",
            "u_identity_provider": "Okta",
            "u_risk_score": "10",
            "sys_created_on": automation_time,
            "sys_updated_on": automation_time,
        }
    )
    return users


def make_cmdb(rng: random.Random, users: list[dict[str, str]]) -> list[dict[str, str]]:
    ci_specs = [
        ("vpn-gw-01", "cmdb_ci_netgear", "Corporate VPN", "Network Operations", "Cisco IOS XE 17", "10.20.1.10"),
        ("vpn-gw-02", "cmdb_ci_netgear", "Corporate VPN", "Network Operations", "Cisco IOS XE 17", "10.20.1.11"),
        ("idp-prd-01", "cmdb_ci_appl", "Customer Identity", "Identity and Access", "Red Hat Enterprise Linux 9", "10.30.4.20"),
        ("edr-mgmt-01", "cmdb_ci_server", "Security Monitoring", "Endpoint Engineering", "Windows Server 2022", "10.25.7.15"),
        ("siem-hf-01", "cmdb_ci_linux_server", "Security Monitoring", "Security Operations", "Ubuntu Server 22.04 LTS", "10.25.8.21"),
        ("waf-edge-02", "cmdb_ci_netgear", "Online Banking", "Network Operations", "Cisco IOS XE 17", "10.20.2.32"),
        ("prd-pay-api-01", "cmdb_ci_appl", "Payments API", "Application Support", "Amazon Linux 2023", "10.40.11.50"),
        ("prd-pay-api-02", "cmdb_ci_appl", "Payments API", "Application Support", "Amazon Linux 2023", "10.40.11.51"),
        ("prd-sql-pay-01", "cmdb_ci_database", "Card Processing", "Database Services", "Microsoft SQL Server 2022", "10.40.30.80"),
        ("prd-sql-pay-02", "cmdb_ci_database", "Card Processing", "Database Services", "Microsoft SQL Server 2022", "10.40.30.81"),
        ("dw-etl-01", "cmdb_ci_linux_server", "Data Warehouse", "Linux Platform", "Red Hat Enterprise Linux 9", "10.45.9.17"),
        ("fin-erp-01", "cmdb_ci_appl", "ERP Finance", "Application Support", "Windows Server 2022", "10.41.20.12"),
        ("claims-web-03", "cmdb_ci_appl", "Claims Portal", "Application Support", "Ubuntu Server 22.04 LTS", "10.42.6.33"),
        ("mes-hmi-07", "cmdb_ci_computer", "Manufacturing MES", "Endpoint Engineering", "Windows 11 Enterprise", "10.60.14.107"),
        ("mail-edge-01", "cmdb_ci_server", "Email and Collaboration", "Windows Server", "Windows Server 2022", "10.35.2.25"),
    ]

    for index in range(1, 41):
        service = rng.choice(BUSINESS_SERVICES)
        group = rng.choice(SUPPORT_GROUPS)
        ci_class = rng.choice(CI_CLASSES)
        os_name = rng.choice(OS_CHOICES)
        octet = 100 + index
        name_prefix = "lt" if ci_class == "cmdb_ci_computer" else rng.choice(["app", "db", "web", "job", "node"])
        ci_specs.append(
            (
                f"{name_prefix}-{service.lower().replace(' ', '-')[:8]}-{index:02d}",
                ci_class,
                service,
                group,
                os_name,
                f"10.{rng.randint(50, 70)}.{rng.randint(1, 240)}.{octet}",
            )
        )

    rows: list[dict[str, str]] = []
    for index, (name, ci_class, service, group, os_name, ip_address) in enumerate(ci_specs, start=1):
        created = random_time(rng, 180, 900)
        updated = random_time(rng, 0, 60)
        env = rng.choices(["prod", "stage", "dev", "lab"], weights=[68, 14, 13, 5])[0]
        criticality = rng.choices(["1 - most critical", "2 - high", "3 - medium", "4 - low"], weights=[14, 32, 42, 12])[0]
        owner = rng.choice(users)
        rows.append(
            {
                "sys_id": sys_id(rng),
                "name": name,
                "fqdn": f"{name}.corp.northwind.example",
                "ip_address": ip_address,
                "mac_address": f"02:42:{index:02x}:{rng.randint(0,255):02x}:{rng.randint(0,255):02x}:{rng.randint(0,255):02x}",
                "asset_tag": f"NW-{100000 + index}",
                "serial_number": f"SN{rng.randint(10000000, 99999999)}",
                "sys_class_name": ci_class,
                "install_status": rng.choices(["Installed", "In Maintenance", "Retired"], weights=[88, 9, 3])[0],
                "operational_status": rng.choices(["Operational", "Degraded", "Non-Operational"], weights=[87, 10, 3])[0],
                "environment": env,
                "business_service": service,
                "support_group": group,
                "owned_by": owner["name"],
                "managed_by": rng.choice(users)["name"],
                "location": rng.choice(LOCATIONS),
                "os": os_name,
                "manufacturer": rng.choice(["Dell", "HPE", "Cisco", "Lenovo", "Microsoft", "Amazon Web Services"]),
                "model_id": rng.choice(["PowerEdge R650", "ProLiant DL360", "CSR1000v", "ThinkPad T14", "EC2 m7i.large"]),
                "u_criticality": criticality,
                "u_contains_pii": "true" if service in {"Claims Portal", "Customer Identity", "Online Banking"} else "false",
                "u_pci_scope": "true" if service in {"Card Processing", "Payments API"} else "false",
                "u_edr_status": rng.choices(["Healthy", "Sensor Offline", "Outdated Policy"], weights=[83, 10, 7])[0],
                "u_backup_tier": rng.choice(["gold", "silver", "bronze", "none"]),
                "tags": ",".join(sorted({service.lower().replace(" ", "_"), env, group.lower().replace(" ", "_")})),
                "sys_created_on": snow_time(created),
                "sys_updated_on": snow_time(max(created, updated)),
            }
        )
    return rows


def make_changes(rng: random.Random, users: list[dict[str, str]], cis: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    special = [
        {
            "number": "CHG0030001",
            "type": "Emergency",
            "short_description": "Block malicious VPN source ranges after credential stuffing detection",
            "description": "Threat Response approved emergency controls for repeated failed VPN authentication from high-risk networks.",
            "category": "Security",
            "risk": "High",
            "impact": "2 - Medium",
            "state": "Closed",
            "business_service": "Corporate VPN",
            "assignment_group": "Threat Response",
            "u_splunk_notable_event_id": "NE-2026-05-18-0007",
            "u_splunk_correlation_search": "ESCU - Excessive VPN Authentication Failures",
        },
        {
            "number": "CHG0030002",
            "type": "Normal",
            "short_description": "Apply SQL cumulative update to card processing database cluster",
            "description": "Monthly database patching for PCI-scoped payment databases with application team validation.",
            "category": "Software",
            "risk": "Moderate",
            "impact": "1 - High",
            "state": "Review",
            "business_service": "Card Processing",
            "assignment_group": "Database Services",
            "u_splunk_notable_event_id": "",
            "u_splunk_correlation_search": "",
        },
        {
            "number": "CHG0030003",
            "type": "Emergency",
            "short_description": "Disable vulnerable edge WAF rule package and deploy vendor hotfix",
            "description": "Emergency remediation after exploit traffic was observed against the online banking perimeter.",
            "category": "Network",
            "risk": "High",
            "impact": "1 - High",
            "state": "Closed",
            "business_service": "Online Banking",
            "assignment_group": "Network Operations",
            "u_splunk_notable_event_id": "NE-2026-05-20-0014",
            "u_splunk_correlation_search": "ESCU - Web Exploit Attempt Against Internet Facing Server",
        },
    ]

    for item in special:
        ci = rng.choice([ci for ci in cis if ci["business_service"] == item["business_service"]])
        opened = BASE_TIME - timedelta(days=rng.randint(5, 12), hours=rng.randint(1, 12))
        start = opened + timedelta(hours=rng.randint(2, 10))
        end = start + timedelta(hours=rng.randint(1, 4))
        rows.append(make_change_row(rng, users, ci, item, opened, start, end))

    categories = ["Security", "Software", "Hardware", "Network", "Database", "Cloud", "Application"]
    templates = [
        "Rotate service certificate for {service}",
        "Patch operating system on {ci}",
        "Update firewall policy for {service}",
        "Deploy application release to {service}",
        "Increase database storage for {ci}",
        "Replace failed disk on {ci}",
        "Tune EDR policy for {service}",
        "Add monitoring for {ci}",
        "Refresh TLS configuration on {ci}",
        "Modify load balancer pool for {service}",
    ]

    for offset in range(4, 46):
        ci = rng.choice(cis)
        opened = random_time(rng, 1, 90)
        start = opened + timedelta(hours=rng.randint(4, 72))
        end = start + timedelta(hours=rng.randint(1, 8))
        state = rng.choices(["Scheduled", "Implement", "Review", "Closed", "Cancelled"], weights=[20, 10, 12, 52, 6])[0]
        if state in {"Closed", "Cancelled"}:
            updated = end + timedelta(hours=rng.randint(1, 12))
        else:
            updated = opened + timedelta(hours=rng.randint(1, 48))
        item = {
            "number": f"CHG003{offset:04d}",
            "type": rng.choices(["Normal", "Standard", "Emergency"], weights=[72, 20, 8])[0],
            "short_description": rng.choice(templates).format(service=ci["business_service"], ci=ci["name"]),
            "description": f"Generated demo change for {ci['business_service']} affecting {ci['name']}.",
            "category": rng.choice(categories),
            "risk": rng.choices(["Low", "Moderate", "High"], weights=[42, 44, 14])[0],
            "impact": rng.choice(["1 - High", "2 - Medium", "3 - Low"]),
            "state": state,
            "business_service": ci["business_service"],
            "assignment_group": ci["support_group"],
            "u_splunk_notable_event_id": "",
            "u_splunk_correlation_search": "",
            "sys_updated_on_override": updated,
        }
        rows.append(make_change_row(rng, users, ci, item, opened, start, end))

    return rows


def make_change_row(
    rng: random.Random,
    users: list[dict[str, str]],
    ci: dict[str, str],
    item: dict[str, str],
    opened: datetime,
    start: datetime,
    end: datetime,
) -> dict[str, str]:
    requester = rng.choice(users)
    assignee = rng.choice(users)
    closed = item["state"] in {"Closed", "Cancelled"}
    updated = item.get("sys_updated_on_override") or (end + timedelta(hours=rng.randint(1, 10)) if closed else opened + timedelta(hours=2))
    return {
        "sys_id": sys_id(rng),
        "number": item["number"],
        "type": item["type"],
        "state": item["state"],
        "approval": "Approved" if item["state"] != "Cancelled" else "Rejected",
        "risk": item["risk"],
        "impact": item["impact"],
        "priority": item["impact"],
        "category": item["category"],
        "assignment_group": item["assignment_group"],
        "assigned_to": assignee["name"],
        "requested_by": requester["name"],
        "opened_by": requester["name"],
        "business_service": item["business_service"],
        "cmdb_ci": ci["name"],
        "short_description": item["short_description"],
        "description": item["description"],
        "justification": "Demo change record created to support Splunk Enterprise Security storytelling.",
        "implementation_plan": "Validate pre-checks, implement approved change, monitor service health, and document results.",
        "backout_plan": "Restore previous configuration or package version and notify the service owner.",
        "test_plan": "Confirm service availability, authentication flow, and alert telemetry after implementation.",
        "start_date": snow_time(start),
        "end_date": snow_time(end),
        "work_start": snow_time(start if closed else None),
        "work_end": snow_time(end if closed else None),
        "close_code": rng.choice(["Successful", "Successful with Issues", "Unsuccessful"]) if closed else "",
        "close_notes": "Change completed and monitoring returned to normal." if closed else "",
        "u_environment": ci["environment"],
        "u_splunk_notable_event_id": item["u_splunk_notable_event_id"],
        "u_splunk_correlation_search": item["u_splunk_correlation_search"],
        "sys_created_on": snow_time(opened),
        "opened_at": snow_time(opened),
        "sys_updated_on": snow_time(max(opened, updated)),
    }


SECURITY_TEMPLATES = [
    (
        "Security",
        "Credential Access",
        "Multiple failed VPN logins followed by success for {user}",
        "Splunk ES detected repeated authentication failures followed by a successful VPN login for {user}.",
        "Credential Access",
        "T1110",
        "ESCU - Excessive VPN Authentication Failures",
    ),
    (
        "Security",
        "Malware",
        "EDR malware quarantine on {ci}",
        "Endpoint detection quarantined suspicious payload and submitted telemetry for triage.",
        "Execution",
        "T1204",
        "ESCU - Malware Outbreak Detected",
    ),
    (
        "Security",
        "Data Loss",
        "Unusual outbound data transfer from {ci}",
        "Splunk ES risk rules identified high-volume outbound transfer outside the normal peer group.",
        "Exfiltration",
        "T1041",
        "ESCU - High Volume Data Transfer to External Destination",
    ),
    (
        "Security",
        "Privilege Escalation",
        "Privileged group membership change for {user}",
        "Identity audit logs showed a privileged group membership change requiring validation.",
        "Privilege Escalation",
        "T1098",
        "ESCU - Windows AD Privileged Group Modification",
    ),
    (
        "Security",
        "Defense Evasion",
        "EDR sensor offline on critical asset {ci}",
        "Critical asset stopped reporting EDR telemetry during active investigation window.",
        "Defense Evasion",
        "T1562",
        "ESCU - Endpoint Security Agent Tampering",
    ),
]

IT_TEMPLATES = [
    ("Network", "VPN", "VPN users report intermittent disconnects", "Users report VPN reconnects during peak business hours."),
    ("Database", "Performance", "High database latency on {ci}", "Application owners report elevated query latency."),
    ("Application", "Availability", "{service} transaction failures", "Synthetic monitoring shows transaction failures above threshold."),
    ("Software", "Patch", "Patch validation failed on {ci}", "Automated patch job reported failed post-install validation."),
    ("Hardware", "Disk", "Disk capacity warning on {ci}", "Filesystem utilization crossed operational threshold."),
    ("Cloud", "Access", "Cloud role assignment review requested", "Access governance workflow requires owner approval."),
    ("Email", "Phishing", "User-reported suspicious email", "Employee reported suspicious email through the phishing add-in."),
]


def make_incidents(
    rng: random.Random,
    users: list[dict[str, str]],
    cis: list[dict[str, str]],
    changes: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    automation_user = next(user for user in users if user["user_name"] == "soc_automation")

    scenario_defs = [
        ("INC0010001", "1 - High", "1 - High", "vpn-gw-01", "Multiple failed VPN logins followed by success for JPatel", "NE-2026-05-18-0007"),
        ("INC0010002", "1 - High", "2 - Medium", "edr-mgmt-01", "EDR malware quarantine on fin-lt-014", "NE-2026-05-19-0009"),
        ("INC0010003", "1 - High", "1 - High", "prd-sql-pay-01", "High database latency after card processing patch", ""),
        ("INC0010004", "2 - Medium", "1 - High", "waf-edge-02", "Web exploit attempt against online banking perimeter", "NE-2026-05-20-0014"),
        ("INC0010005", "1 - High", "2 - Medium", "dw-etl-01", "Unusual outbound data transfer from dw-etl-01", "NE-2026-05-21-0004"),
        ("INC0010006", "2 - Medium", "2 - Medium", "idp-prd-01", "Privileged group membership change for AReed", "NE-2026-05-22-0006"),
    ]

    for index, (number, impact, urgency, ci_name, short_description, notable_id) in enumerate(scenario_defs):
        ci = next((record for record in cis if record["name"] == ci_name), rng.choice(cis))
        opened = BASE_TIME - timedelta(days=9 - index, hours=rng.randint(1, 8), minutes=rng.randint(0, 59))
        security_template = SECURITY_TEMPLATES[index % len(SECURITY_TEMPLATES)]
        rows.append(
            make_incident_row(
                rng=rng,
                number=number,
                caller=automation_user,
                users=users,
                ci=ci,
                opened=opened,
                category=security_template[0],
                subcategory=security_template[1],
                impact=impact,
                urgency=urgency,
                short_description=short_description,
                description=security_template[3].format(user="JPatel", ci=ci["name"], service=ci["business_service"]),
                assignment_group="Security Operations",
                state="Resolved",
                close_code="Solved Remotely (Permanently)",
                notable_id=notable_id,
                correlation_search=security_template[6],
                mitre_tactic=security_template[4],
                mitre_technique=security_template[5],
                caused_by=changes[index % len(changes)]["number"] if index in {2, 3} else "",
            )
        )

    for offset in range(7, 151):
        ci = rng.choice(cis)
        caller = rng.choice(users)
        is_security = rng.random() < 0.38
        opened = random_time(rng, 0, 90)
        impact = rng.choices(["1 - High", "2 - Medium", "3 - Low"], weights=[13, 42, 45])[0]
        urgency = rng.choices(["1 - High", "2 - Medium", "3 - Low"], weights=[16, 45, 39])[0]
        state = rng.choices(["New", "In Progress", "On Hold", "Resolved", "Closed"], weights=[8, 20, 8, 38, 26])[0]
        if is_security:
            template = rng.choice(SECURITY_TEMPLATES)
            user_label = rng.choice(users)["user_name"]
            category, subcategory, short_template, desc_template, tactic, technique, search = template
            assignment_group = rng.choice(["Security Operations", "Threat Response", "Identity and Access"])
            notable_id = f"NE-2026-{opened.month:02d}-{opened.day:02d}-{rng.randint(1, 9999):04d}" if rng.random() < 0.42 else ""
            short_description = short_template.format(user=user_label, ci=ci["name"], service=ci["business_service"])
            description = desc_template.format(user=user_label, ci=ci["name"], service=ci["business_service"])
        else:
            template = rng.choice(IT_TEMPLATES)
            category, subcategory, short_template, desc_template = template
            tactic = technique = search = notable_id = ""
            assignment_group = ci["support_group"]
            short_description = short_template.format(ci=ci["name"], service=ci["business_service"])
            description = desc_template.format(ci=ci["name"], service=ci["business_service"])

        close_code = rng.choice(["Solved Remotely (Permanently)", "Solved Work Around", "Not Solved (Not Reproducible)"]) if state in {"Resolved", "Closed"} else ""
        caused_by = rng.choice(changes)["number"] if rng.random() < 0.08 else ""
        rows.append(
            make_incident_row(
                rng=rng,
                number=f"INC001{offset:04d}",
                caller=caller,
                users=users,
                ci=ci,
                opened=opened,
                category=category,
                subcategory=subcategory,
                impact=impact,
                urgency=urgency,
                short_description=short_description,
                description=description,
                assignment_group=assignment_group,
                state=state,
                close_code=close_code,
                notable_id=notable_id,
                correlation_search=search,
                mitre_tactic=tactic,
                mitre_technique=technique,
                caused_by=caused_by,
            )
        )

    return rows


def make_incident_row(
    rng: random.Random,
    number: str,
    caller: dict[str, str],
    users: list[dict[str, str]],
    ci: dict[str, str],
    opened: datetime,
    category: str,
    subcategory: str,
    impact: str,
    urgency: str,
    short_description: str,
    description: str,
    assignment_group: str,
    state: str,
    close_code: str,
    notable_id: str,
    correlation_search: str,
    mitre_tactic: str,
    mitre_technique: str,
    caused_by: str,
) -> dict[str, str]:
    priority = priority_for(impact, urgency)
    assigned_to = rng.choice(users)
    resolved_by = rng.choice(users) if state in {"Resolved", "Closed"} else None
    updated = opened + timedelta(hours=rng.randint(1, 96), minutes=rng.randint(0, 59))
    resolved_at = updated if state in {"Resolved", "Closed"} else None
    closed_at = resolved_at + timedelta(hours=rng.randint(1, 24)) if state == "Closed" and resolved_at else None
    security_record = category == "Security"
    return {
        "sys_id": sys_id(rng),
        "number": number,
        "state": state,
        "incident_state": state,
        "active": "false" if state in {"Resolved", "Closed"} else "true",
        "category": category,
        "subcategory": subcategory,
        "contact_type": rng.choice(["self-service", "phone", "email", "monitoring", "event"]),
        "caller_id": caller["name"],
        "opened_by": caller["name"],
        "assigned_to": assigned_to["name"],
        "assignment_group": assignment_group,
        "business_service": ci["business_service"],
        "cmdb_ci": ci["name"],
        "company": caller["company"],
        "location": caller["location"],
        "impact": impact,
        "urgency": urgency,
        "priority": priority,
        "severity": priority,
        "short_description": short_description,
        "description": description,
        "work_notes": work_notes_for(category, notable_id, ci["name"]),
        "close_code": close_code,
        "close_notes": "Demo record resolved after triage, containment, and validation." if resolved_at else "",
        "resolved_by": resolved_by["name"] if resolved_by else "",
        "caused_by": caused_by,
        "problem_id": "",
        "parent_incident": "",
        "reopen_count": str(rng.choices([0, 1, 2], weights=[84, 13, 3])[0]),
        "u_security_incident": "true" if security_record else "false",
        "u_splunk_notable_event_id": notable_id,
        "u_splunk_correlation_search": correlation_search,
        "u_mitre_tactic": mitre_tactic,
        "u_mitre_technique": mitre_technique,
        "u_es_risk_object": ci["name"] if security_record else "",
        "u_es_risk_score": str(rng.randint(35, 95)) if security_record else "",
        "sys_created_on": snow_time(opened),
        "opened_at": snow_time(opened),
        "resolved_at": snow_time(resolved_at),
        "closed_at": snow_time(closed_at),
        "sys_updated_on": snow_time(max(value for value in [opened, updated, resolved_at, closed_at] if value is not None)),
    }


def work_notes_for(category: str, notable_id: str, ci_name: str) -> str:
    if category == "Security":
        notable_text = f" Splunk notable {notable_id} linked." if notable_id else ""
        return f"SOC triage opened from Splunk ES correlation results for {ci_name}.{notable_text}"
    return f"Service desk triage notes captured for {ci_name}; owner group notified."


def make_task_ci_links(
    rng: random.Random,
    incidents: list[dict[str, str]],
    changes: list[dict[str, str]],
    cis: list[dict[str, str]],
) -> list[dict[str, str]]:
    ci_by_name = {ci["name"]: ci for ci in cis}
    links: list[TaskLink] = []

    for incident in incidents:
        ci = ci_by_name[incident["cmdb_ci"]]
        links.append(TaskLink(incident["number"], incident["sys_id"], "incident", ci["name"], ci["sys_id"], "Affected CI"))
        if rng.random() < 0.18:
            other = rng.choice(cis)
            links.append(TaskLink(incident["number"], incident["sys_id"], "incident", other["name"], other["sys_id"], "Related CI"))

    for change in changes:
        ci = ci_by_name[change["cmdb_ci"]]
        links.append(TaskLink(change["number"], change["sys_id"], "change_request", ci["name"], ci["sys_id"], "Planned CI"))
        if rng.random() < 0.3:
            other = rng.choice([record for record in cis if record["business_service"] == change["business_service"]])
            links.append(TaskLink(change["number"], change["sys_id"], "change_request", other["name"], other["sys_id"], "Impacted CI"))

    rows = []
    for link in links:
        rows.append(
            {
                "sys_id": sys_id(rng),
                "task": link.task_number,
                "task_sys_id": link.task_sys_id,
                "table": link.table,
                "ci_item": link.ci_name,
                "ci_sys_id": link.ci_sys_id,
                "relationship_type": link.relationship_type,
                "sys_created_on": snow_time(random_time(rng, 0, 90)),
                "sys_updated_on": snow_time(random_time(rng, 0, 30)),
            }
        )
    return rows


def make_es_incidents(rng: random.Random, incidents: list[dict[str, str]]) -> list[dict[str, str]]:
    """Create ES notable-source rows that can become Mission Control incidents."""
    security_incidents = [
        incident
        for incident in incidents
        if incident["u_security_incident"] == "true" and incident["u_splunk_notable_event_id"]
    ]
    fallback_security_incidents = [
        incident for incident in incidents if incident["u_security_incident"] == "true"
    ]
    source_incidents: list[dict[str, str]] = []
    seen_incidents: set[str] = set()
    for incident in security_incidents + fallback_security_incidents:
        if incident["number"] in seen_incidents:
            continue
        source_incidents.append(incident)
        seen_incidents.add(incident["number"])
        if len(source_incidents) == 18:
            break

    queues = ("SOC 1 Queue", "SOC 2 Queue")
    statuses = ("New", "In Progress", "New", "In Progress", "On Hold")
    rows: list[dict[str, str]] = []

    for index, incident in enumerate(source_incidents, start=1):
        queue = queues[(index - 1) % len(queues)]
        notable_id = incident["u_splunk_notable_event_id"] or f"NE-{BASE_TIME:%Y-%m-%d}-{index:04d}"
        mc_incident_id = f"MC-{BASE_TIME:%Y%m%d}-{index:04d}"
        finding_id = f"FINDING-{BASE_TIME:%Y%m%d}-{index:04d}"
        created = parse_snow_time(incident["opened_at"]) or random_time(rng, 0, 7)
        updated = parse_snow_time(incident["sys_updated_on"]) or (created + timedelta(hours=1))
        severity = cim_severity(incident["priority"])
        urgency = {
            "critical": "critical",
            "high": "high",
            "medium": "medium",
            "low": "low",
        }.get(severity, "medium")
        soc_level = "SOC 1" if queue == "SOC 1 Queue" else "SOC 2"
        analyst = "soc1_triage" if soc_level == "SOC 1" else "soc2_investigator"

        rows.append(
            {
                "_time": json_time(updated),
                "time": snow_time(updated),
                "timestamp": json_time(updated),
                "id": mc_incident_id,
                "incident_id": mc_incident_id,
                "display_id": mc_incident_id,
                "finding_id": finding_id,
                "notable_id": notable_id,
                "event_id": notable_id,
                "name": f"{incident['number']} - {incident['short_description']}",
                "title": f"{incident['number']} - {incident['short_description']}",
                "description": (
                    f"Splunk ES notable {notable_id} is linked to ServiceNow case "
                    f"{incident['number']} for {incident['business_service']} on {incident['cmdb_ci']}."
                ),
                "summary": (
                    f"{soc_level} triage item for {incident['number']}: "
                    f"{incident['short_description']}"
                ),
                "source": incident["u_splunk_correlation_search"],
                "source_type": "Splunk Enterprise Security notable event",
                "incident_origin": "Splunk Enterprise Security",
                "incident_type": "ES Notable",
                "soc_queue": queue,
                "queue": queue,
                "security_domain": soc_level,
                "status_name": statuses[(index - 1) % len(statuses)],
                "status": statuses[(index - 1) % len(statuses)].lower().replace(" ", "_"),
                "disposition": "Undetermined",
                "urgency": urgency,
                "severity": severity,
                "sensitivity": "amber",
                "assignee": analyst,
                "owner": analyst,
                "snow_incident_number": incident["number"],
                "service_now_incident": incident["number"],
                "external_reference": incident["number"],
                "external_url_label": f"ServiceNow {incident['number']}",
                "cmdb_ci": incident["cmdb_ci"],
                "dest": incident["cmdb_ci"],
                "risk_object": incident["u_es_risk_object"] or incident["cmdb_ci"],
                "risk_score": incident["u_es_risk_score"] or str(rng.randint(35, 95)),
                "business_service": incident["business_service"],
                "priority": incident["priority"],
                "assignment_group": incident["assignment_group"],
                "mitre_tactic": incident["u_mitre_tactic"],
                "mitre_technique": incident["u_mitre_technique"],
                "correlation_search": incident["u_splunk_correlation_search"],
                "rule_name": incident["u_splunk_correlation_search"],
                "create_time": str(int(created.timestamp())),
                "update_time": str(int(updated.timestamp())),
                "mc_create_time": str(int(created.timestamp())),
                "sla_expiry_time": str(int((created + timedelta(hours=24 if urgency in {"critical", "high"} else 72)).timestamp())),
                "src": "",
                "src_user": incident["src_user"],
                "user": incident["user"],
                "vendor": "Splunk",
                "product": "Enterprise Security",
                "vendor_product": "Splunk Enterprise Security",
            }
        )

    return rows



def cim_common_fields(data_model: str, dataset: str, tag: str) -> dict[str, str]:
    return {
        "vendor": SNOW_VENDOR,
        "product": SNOW_PRODUCT,
        "vendor_product": SNOW_VENDOR_PRODUCT,
        "dvc": SNOW_INSTANCE,
        "instance": "synthetic-demo",
        "cim_data_model": data_model,
        "cim_dataset": dataset,
        "tag": tag,
    }


def ticket_action(state: str) -> str:
    if state in {"New", "Scheduled"}:
        return "created"
    if state == "Cancelled":
        return "updated"
    return "updated"


def ticket_status(state: str, approval: str = "", close_code: str = "") -> str:
    if state == "Cancelled" or approval == "Rejected" or close_code == "Unsuccessful":
        return "failure"
    return "success"


def cim_severity(priority: str) -> str:
    if "Critical" in priority:
        return "critical"
    if "High" in priority:
        return "high"
    if "Moderate" in priority:
        return "medium"
    if "Low" in priority:
        return "low"
    return "informational"


def identity_priority(user: dict[str, str]) -> str:
    if user.get("vip") == "true":
        return "critical"
    risk_score = int(user.get("u_risk_score") or 0)
    if risk_score >= 70:
        return "high"
    if risk_score >= 40:
        return "medium"
    return "low"


def add_cim_fields(
    users: list[dict[str, str]],
    cis: list[dict[str, str]],
    changes: list[dict[str, str]],
    incidents: list[dict[str, str]],
    task_ci: list[dict[str, str]],
) -> None:
    """Add Splunk CIM-friendly fields while preserving raw ServiceNow fields."""

    for user in users:
        priority = identity_priority(user)
        user.update(
            {
                **cim_common_fields("Identity", "Identity", "identity"),
                "identity": user["user_name"],
                "user": user["user_name"],
                "src_user": user["user_name"],
                "user_id": user["employee_number"],
                "user_email": user["email"],
                "user_bunit": user["department"],
                "user_category": user["title"],
                "user_priority": priority,
                "priority": priority,
                "managed_by": user["manager"] or "unassigned",
                "user_manager": user["manager"] or "unassigned",
                "status": "success" if user["active"] == "true" else "failure",
                "result": "active" if user["active"] == "true" else "inactive",
            }
        )

    for ci in cis:
        ci.update(
            {
                **cim_common_fields("Inventory", "All_Inventory", "inventory"),
                "dest": ci["name"],
                "dest_name": ci["name"],
                "dest_host": ci["name"],
                "dest_ip": ci["ip_address"],
                "ip": ci["ip_address"],
                "dns": ci["fqdn"],
                "nt_host": ci["name"],
                "mac": ci["mac_address"].lower(),
                "owner": ci["owned_by"],
                "description": f"{ci['business_service']} {ci['sys_class_name']}",
                "vendor": ci["manufacturer"],
                "product": ci["model_id"],
                "vendor_product": f"{ci['manufacturer']} {ci['model_id']}",
                "status": ci["operational_status"].lower().replace(" ", "_"),
            }
        )

    for change in changes:
        status = ticket_status(change["state"], change.get("approval", ""), change.get("close_code", ""))
        change.update(
            {
                **cim_common_fields("Change", "All_Changes", "change"),
                "action": ticket_action(change["state"]),
                "change_type": "service_management",
                "object": change["cmdb_ci"],
                "object_id": change["sys_id"],
                "object_category": change["category"],
                "object_type": "change_request",
                "object_attrs": f"business_service={change['business_service']},risk={change['risk']},type={change['type']}",
                "result": change["state"],
                "result_id": change["number"],
                "status": status,
                "user": change["requested_by"],
                "src_user": change["opened_by"],
                "dest": change["cmdb_ci"],
                "dest_name": change["cmdb_ci"],
                "severity": cim_severity(change["priority"]),
                "ticket_id": change["number"],
                "ticket_type": "change_request",
                "ticket_status": change["state"],
            }
        )

    for incident in incidents:
        status = ticket_status(incident["state"], close_code=incident.get("close_code", ""))
        incident.update(
            {
                **cim_common_fields("Change", "All_Changes", "change"),
                "action": ticket_action(incident["state"]),
                "change_type": "service_management",
                "object": incident["number"],
                "object_id": incident["sys_id"],
                "object_category": incident["category"],
                "object_type": "incident",
                "object_attrs": f"business_service={incident['business_service']},priority={incident['priority']},security_incident={incident['u_security_incident']}",
                "result": incident["state"],
                "result_id": incident["number"],
                "status": status,
                "user": incident["caller_id"],
                "src_user": incident["opened_by"],
                "dest": incident["cmdb_ci"],
                "dest_name": incident["cmdb_ci"],
                "severity": cim_severity(incident["priority"]),
                "ticket_id": incident["number"],
                "ticket_type": "incident",
                "ticket_status": incident["state"],
            }
        )

    for link in task_ci:
        link.update(
            {
                **cim_common_fields("Change", "All_Changes", "change"),
                "action": "updated",
                "change_type": "relationship",
                "object": link["ci_item"],
                "object_id": link["ci_sys_id"],
                "object_category": link["relationship_type"],
                "object_type": link["table"],
                "result": link["relationship_type"],
                "result_id": link["task"],
                "status": "success",
                "user": "servicenow",
                "src_user": "servicenow",
                "dest": link["ci_item"],
                "dest_name": link["ci_item"],
                "ticket_id": link["task"],
                "ticket_type": link["table"],
                "task_table": link["table"],
            }
        )

def write_manifest(dataset_counts: dict[str, int], base_time: datetime) -> None:
    manifest = {
        "name": "Synthetic ServiceNow data for Splunk Enterprise Security demos",
        "generated_at": json_time(base_time),
        "base_time": json_time(base_time),
        "date_mode": "rolling" if base_time != DEFAULT_BASE_TIME else "static",
        "seed": SEED,
        "tables": dataset_counts,
        "service_now_instance": SNOW_INSTANCE,
        "privacy_note": "All names, emails, systems, IP addresses, and records are synthetic demo data.",
        "cim_note": "Rows include raw ServiceNow fields plus Splunk CIM-friendly fields. Splunk eventtype/tag configuration is provided under splunk_app/TA-synthetic-servicenow/default.",
        "suggested_sourcetypes": {
            "incidents": "snow:incident",
            "changes": "snow:change_request",
            "cmdb_ci": "snow:cmdb_ci",
            "users": "snow:sys_user",
            "task_ci": "snow:task_ci",
            "es_incidents": "demo:es:incident",
        },
        "cim_mappings": {
            "incidents": "Change.All_Changes",
            "changes": "Change.All_Changes",
            "task_ci": "Change.All_Changes",
            "cmdb_ci": "Inventory.All_Inventory",
            "users": "Enterprise Security identity lookup-friendly fields",
            "es_incidents": "Mission Control/ES incident source fields",
        },
    }
    (DATASET_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_hec_output_aliases(datasets: dict[str, list[dict[str, str]]], fieldnames: dict[str, list[str]]) -> None:
    """Write CSV filenames expected by send_csv_to_splunk.py."""
    aliases = {
        "incidents": "servicenow_incidents.csv",
        "cmdb_ci": "servicenow_cmdb.csv",
        "changes": "servicenow_changes.csv",
        "users": "servicenow_users.csv",
        "es_incidents": "es_incidents.csv",
    }
    for dataset_name, filename in aliases.items():
        write_csv(OUTPUT_ROOT / filename, datasets[dataset_name], fieldnames[dataset_name])


def main() -> None:
    global BASE_TIME

    args = parse_args()
    BASE_TIME = DEFAULT_BASE_TIME if args.static else parse_base_time(args.base_time)

    rng = random.Random(SEED)
    users = make_users(rng)
    cis = make_cmdb(rng, users)
    changes = make_changes(rng, users, cis)
    incidents = make_incidents(rng, users, cis, changes)
    task_ci = make_task_ci_links(rng, incidents, changes, cis)

    add_cim_fields(users, cis, changes, incidents, task_ci)
    es_incidents = make_es_incidents(rng, incidents)

    datasets = {
        "users": users,
        "cmdb_ci": cis,
        "changes": changes,
        "incidents": incidents,
        "task_ci": task_ci,
        "es_incidents": es_incidents,
    }

    fieldnames = {name: list(rows[0].keys()) for name, rows in datasets.items()}
    write_csv(CSV_ROOT / "servicenow_users.csv", users, fieldnames["users"])
    write_csv(CSV_ROOT / "servicenow_cmdb_ci.csv", cis, fieldnames["cmdb_ci"])
    write_csv(CSV_ROOT / "servicenow_change_requests.csv", changes, fieldnames["changes"])
    write_csv(CSV_ROOT / "servicenow_incidents.csv", incidents, fieldnames["incidents"])
    write_csv(CSV_ROOT / "servicenow_task_ci.csv", task_ci, fieldnames["task_ci"])
    write_csv(MISSION_CONTROL_CSV_ROOT / "es_incidents.csv", es_incidents, fieldnames["es_incidents"])

    write_jsonl(JSONL_ROOT / "servicenow_users.jsonl", users, "sys_user", "servicenow://sys_user")
    write_jsonl(JSONL_ROOT / "servicenow_cmdb_ci.jsonl", cis, "cmdb_ci", "servicenow://cmdb_ci")
    write_jsonl(JSONL_ROOT / "servicenow_change_requests.jsonl", changes, "change_request", "servicenow://change_request")
    write_jsonl(JSONL_ROOT / "servicenow_incidents.jsonl", incidents, "incident", "servicenow://incident")
    write_jsonl(JSONL_ROOT / "servicenow_task_ci.jsonl", task_ci, "task_ci", "servicenow://task_ci")
    write_jsonl(MISSION_CONTROL_JSONL_ROOT / "es_incidents.jsonl", es_incidents, "es_incident", "mission_control://es_incident")

    if not args.skip_output:
        write_hec_output_aliases(datasets, fieldnames)

    write_manifest({name: len(rows) for name, rows in datasets.items()}, BASE_TIME)


if __name__ == "__main__":
    main()

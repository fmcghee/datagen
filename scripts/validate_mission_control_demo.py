#!/usr/bin/env python3
"""Validate synthetic ES incident source data for Mission Control demos."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ES_INCIDENTS = ROOT / "output" / "es_incidents.csv"

REQUIRED_FIELDS = {
    "_time",
    "id",
    "incident_id",
    "finding_id",
    "notable_id",
    "name",
    "description",
    "soc_queue",
    "queue",
    "status_name",
    "urgency",
    "assignee",
    "snow_incident_number",
    "service_now_incident",
    "cmdb_ci",
    "risk_object",
    "correlation_search",
}

EXPECTED_QUEUES = {"SOC 1 Queue", "SOC 2 Queue"}


def main() -> None:
    with ES_INCIDENTS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise AssertionError(f"{ES_INCIDENTS} did not contain any rows")

    queues = {row.get("soc_queue") for row in rows}
    if queues != EXPECTED_QUEUES:
        raise AssertionError(f"Expected queues {EXPECTED_QUEUES}, got {queues}")

    for index, row in enumerate(rows, start=1):
        missing = sorted(field for field in REQUIRED_FIELDS if not row.get(field))
        if missing:
            raise AssertionError(f"row {index} missing required fields: {missing}")
        if row["snow_incident_number"] != row["service_now_incident"]:
            raise AssertionError(f"row {index} has inconsistent ServiceNow incident fields")
        if not row["snow_incident_number"].startswith("INC"):
            raise AssertionError(f"row {index} does not link to an INC number")

    print(f"Validated {len(rows)} ES incident source rows across {sorted(queues)}")


if __name__ == "__main__":
    main()

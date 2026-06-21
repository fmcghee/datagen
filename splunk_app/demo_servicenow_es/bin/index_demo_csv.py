#!/usr/bin/env python3
"""Index bundled demo CSV rows for the ServiceNow ES Demo Splunk app.

Designed to run as a Splunk scripted input. Each CSV row is emitted as one JSON
event on stdout. Splunk applies index and sourcetype from inputs.conf.

Usage (from inputs.conf):
  index_demo_csv.py servicenow_incidents.csv
  index_demo_csv.py --all
  index_demo_csv.py --all --force
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TIME_FIELDS = ("_time", "time", "timestamp", "opened_at")
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)

DATASETS = (
    "servicenow_incidents.csv",
    "servicenow_changes.csv",
    "servicenow_cmdb.csv",
    "servicenow_users.csv",
    "servicenow_task_ci.csv",
    "es_incidents.csv",
)


def parse_timestamp(value: str) -> float:
    timestamp = value.strip()
    try:
        return float(timestamp)
    except ValueError:
        pass

    if timestamp.endswith("Z"):
        timestamp = f"{timestamp[:-1]}+00:00"

    for fmt in TIMESTAMP_FORMATS:
        try:
            parsed = datetime.strptime(timestamp, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.timestamp()
        except ValueError:
            continue

    parsed = datetime.fromisoformat(timestamp)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def parse_event_time(row: dict[str, str]) -> float:
    for field in TIME_FIELDS:
        value = (row.get(field) or "").strip()
        if value:
            return parse_timestamp(value)
    return datetime.now(timezone.utc).timestamp()


def marker_path(csv_name: str) -> Path:
    app_root = Path(__file__).resolve().parent.parent
    local_dir = app_root / "local"
    local_dir.mkdir(parents=True, exist_ok=True)
    safe_name = csv_name.replace("/", "_")
    return local_dir / f"loaded_{safe_name}.marker"


def already_loaded(csv_name: str, force: bool) -> bool:
    if force:
        return False
    marker = marker_path(csv_name)
    return marker.is_file()


def mark_loaded(csv_name: str, count: int) -> None:
    marker = marker_path(csv_name)
    marker.write_text(f"events={count}\n", encoding="utf-8")


def emit_row(row: dict[str, str]) -> None:
    cleaned = {key: value for key, value in row.items() if key and value is not None}
    cleaned["_time"] = parse_event_time(row)
    sys.stdout.write(json.dumps(cleaned, separators=(",", ":")) + "\n")


def index_csv(path: Path, force: bool) -> int:
    if not path.is_file():
        sys.stderr.write(f"Missing CSV file: {path}\n")
        return 0

    if already_loaded(path.name, force):
        sys.stderr.write(f"Skipping {path.name}; already loaded. Use --force to reload.\n")
        return 0

    count = 0
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} does not contain a CSV header")
        for row in reader:
            emit_row(row)
            count += 1

    mark_loaded(path.name, count)
    sys.stderr.write(f"Indexed {count} events from {path.name}\n")
    return count


def main() -> int:
    force = "--force" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    data_dir = Path(__file__).resolve().parent / "data"

    if not args or args[0] == "--all":
        total = 0
        for csv_name in DATASETS:
            total += index_csv(data_dir / csv_name, force)
        return 0 if total >= 0 else 1

    csv_name = args[0]
    index_csv(data_dir / csv_name, force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

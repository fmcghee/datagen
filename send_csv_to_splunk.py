#!/usr/bin/env python3
"""Send generated demo CSV data to Splunk Cloud using HTTP Event Collector.

The script reads supported CSV files from the output/ directory and sends each
row as a JSON event. HEC credentials are read from environment variables so no
secrets are stored in the repository.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_OUTPUT_DIR = Path("output")
TIME_FIELDS = ("_time", "time", "timestamp", "opened_at")


@dataclass(frozen=True)
class CsvInput:
    filename: str
    index: str
    sourcetype: str


CSV_INPUTS = (
    CsvInput("auth.csv", "demo_security", "demo:auth"),
    CsvInput("endpoint.csv", "demo_security", "demo:endpoint"),
    CsvInput("dns.csv", "demo_security", "demo:dns"),
    CsvInput("network.csv", "demo_security", "demo:network"),
    CsvInput("web.csv", "demo_security", "demo:web"),
    CsvInput("servicenow_incidents.csv", "demo_servicenow", "demo:snow:incident"),
    CsvInput("servicenow_cmdb.csv", "demo_servicenow", "demo:snow:cmdb_ci"),
    CsvInput("servicenow_changes.csv", "demo_servicenow", "demo:snow:change"),
    CsvInput("servicenow_users.csv", "demo_servicenow", "demo:snow:user"),
)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send supported CSV demo data from output/ to Splunk HEC."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory containing demo CSV files. Defaults to output/.",
    )
    parser.add_argument(
        "--host",
        default="splunk-es-demo-datagen",
        help="HEC host metadata value. Defaults to splunk-es-demo-datagen.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Read and validate CSV rows without sending events to Splunk.",
    )
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="Fail if any supported CSV file is missing from the output directory.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds for each HEC request. Defaults to 30.",
    )
    return parser.parse_args()


def normalize_hec_url(raw_url: str) -> str:
    url = raw_url.strip().rstrip("/")
    if not url:
        raise ValueError("SPLUNK_HEC_URL is empty")

    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("SPLUNK_HEC_URL must use https for Splunk Cloud HEC")
    if not parsed.netloc:
        raise ValueError("SPLUNK_HEC_URL must include a host")

    if url.endswith("/services/collector/event"):
        return url
    if url.endswith("/services/collector"):
        return f"{url}/event"
    return f"{url}/services/collector/event"


def parse_event_time(row: dict[str, str]) -> float | None:
    for field in TIME_FIELDS:
        value = (row.get(field) or "").strip()
        if value:
            return parse_timestamp(value)
    return None


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

    try:
        parsed = datetime.fromisoformat(timestamp)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.timestamp()
    except ValueError as error:
        raise ValueError(f"unsupported timestamp format: {value!r}") from error


def iter_csv_rows(path: Path) -> Any:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} does not contain a CSV header")
        for row_number, row in enumerate(reader, start=2):
            cleaned_row = {key: value for key, value in row.items() if key is not None}
            yield row_number, cleaned_row


def build_hec_event(row: dict[str, str], csv_input: CsvInput, host: str) -> dict[str, Any]:
    event: dict[str, Any] = {
        "host": host,
        "source": f"csv:{csv_input.filename}",
        "sourcetype": csv_input.sourcetype,
        "index": csv_input.index,
        "event": row,
    }

    event_time = parse_event_time(row)
    if event_time is not None:
        event["time"] = event_time

    return event


def send_hec_event(hec_url: str, hec_token: str, event: dict[str, Any], timeout: float) -> None:
    body = json.dumps(event, separators=(",", ":")).encode("utf-8")
    request = Request(
        hec_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Splunk {hec_token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HEC request failed with HTTP {error.code}: {error_body}") from error
    except URLError as error:
        raise RuntimeError(f"HEC request failed: {error.reason}") from error

    try:
        result = json.loads(response_body)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"HEC returned non-JSON response: {response_body!r}") from error

    if result.get("code") != 0:
        raise RuntimeError(f"HEC returned error response: {result}")


def load_hec_config(dry_run: bool) -> tuple[str, str]:
    if dry_run:
        return "", ""

    raw_url = os.environ.get("SPLUNK_HEC_URL", "")
    token = os.environ.get("SPLUNK_HEC_TOKEN", "")
    if not raw_url or not token:
        raise RuntimeError(
            "SPLUNK_HEC_URL and SPLUNK_HEC_TOKEN must be set unless --dry-run is used"
        )
    return normalize_hec_url(raw_url), token


def process_file(
    csv_input: CsvInput,
    output_dir: Path,
    host: str,
    hec_url: str,
    hec_token: str,
    timeout: float,
    dry_run: bool,
) -> int:
    path = output_dir / csv_input.filename
    sent_count = 0

    for row_number, row in iter_csv_rows(path):
        try:
            event = build_hec_event(row, csv_input, host)
        except ValueError as error:
            raise ValueError(f"{path}:{row_number}: {error}") from error

        if dry_run:
            sent_count += 1
            continue

        send_hec_event(hec_url, hec_token, event, timeout)
        sent_count += 1

    return sent_count


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir

    if not output_dir.is_dir():
        print(f"Output directory not found: {output_dir}", file=sys.stderr)
        return 1

    missing_files = [csv_input.filename for csv_input in CSV_INPUTS if not (output_dir / csv_input.filename).is_file()]
    if missing_files:
        missing_list = ", ".join(missing_files)
        message = f"Missing supported CSV files in {output_dir}: {missing_list}"
        if args.require_all:
            print(message, file=sys.stderr)
            return 1
        print(f"Warning: {message}", file=sys.stderr)

    available_inputs = [csv_input for csv_input in CSV_INPUTS if (output_dir / csv_input.filename).is_file()]
    if not available_inputs:
        print(f"No supported CSV files found in {output_dir}", file=sys.stderr)
        return 1

    try:
        hec_url, hec_token = load_hec_config(args.dry_run)
    except (RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    total_count = 0
    started_at = time.monotonic()
    for csv_input in available_inputs:
        try:
            count = process_file(
                csv_input=csv_input,
                output_dir=output_dir,
                host=args.host,
                hec_url=hec_url,
                hec_token=hec_token,
                timeout=args.timeout,
                dry_run=args.dry_run,
            )
        except (OSError, RuntimeError, ValueError) as error:
            print(f"Failed processing {csv_input.filename}: {error}", file=sys.stderr)
            return 1

        total_count += count
        action = "Validated" if args.dry_run else "Sent"
        print(f"{action} {count} events from {csv_input.filename} -> {csv_input.index}/{csv_input.sourcetype}")

    elapsed = time.monotonic() - started_at
    action = "Validated" if args.dry_run else "Sent"
    print(f"{action} {total_count} total events in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate synthetic ServiceNow demo data has required CIM-friendly fields."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "datasets" / "servicenow"

CSV_FILES = {
    "users": DATASET_ROOT / "csv" / "servicenow_users.csv",
    "cmdb_ci": DATASET_ROOT / "csv" / "servicenow_cmdb_ci.csv",
    "changes": DATASET_ROOT / "csv" / "servicenow_change_requests.csv",
    "incidents": DATASET_ROOT / "csv" / "servicenow_incidents.csv",
    "task_ci": DATASET_ROOT / "csv" / "servicenow_task_ci.csv",
}

JSONL_FILES = {
    "users": DATASET_ROOT / "jsonl" / "servicenow_users.jsonl",
    "cmdb_ci": DATASET_ROOT / "jsonl" / "servicenow_cmdb_ci.jsonl",
    "changes": DATASET_ROOT / "jsonl" / "servicenow_change_requests.jsonl",
    "incidents": DATASET_ROOT / "jsonl" / "servicenow_incidents.jsonl",
    "task_ci": DATASET_ROOT / "jsonl" / "servicenow_task_ci.jsonl",
}

COMMON_FIELDS = {"vendor", "product", "vendor_product", "dvc", "cim_data_model", "cim_dataset", "tag"}
CHANGE_FIELDS = COMMON_FIELDS | {
    "action",
    "change_type",
    "object",
    "object_id",
    "object_category",
    "object_type",
    "result",
    "result_id",
    "status",
    "user",
    "src_user",
    "dest",
    "ticket_id",
    "ticket_type",
}
INVENTORY_FIELDS = COMMON_FIELDS | {
    "dest",
    "dest_name",
    "dest_host",
    "dest_ip",
    "ip",
    "dns",
    "nt_host",
    "mac",
    "owner",
    "status",
}
IDENTITY_FIELDS = COMMON_FIELDS | {
    "identity",
    "user",
    "user_id",
    "user_email",
    "user_bunit",
    "user_category",
    "user_priority",
    "managed_by",
    "status",
}

REQUIRED_BY_DATASET = {
    "users": IDENTITY_FIELDS,
    "cmdb_ci": INVENTORY_FIELDS,
    "changes": CHANGE_FIELDS,
    "incidents": CHANGE_FIELDS,
    "task_ci": CHANGE_FIELDS,
}

EXPECTED_MODELS = {
    "users": "Identity",
    "cmdb_ci": "Inventory",
    "changes": "Change",
    "incidents": "Change",
    "task_ci": "Change",
}

EXPECTED_TAGS = {
    "users": "identity",
    "cmdb_ci": "inventory",
    "changes": "change",
    "incidents": "change",
    "task_ci": "change",
}

EXPECTED_JSONL_TABLES = {
    "users": "sys_user",
    "cmdb_ci": "cmdb_ci",
    "changes": "change_request",
    "incidents": "incident",
    "task_ci": "task_ci",
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def assert_required_fields(dataset: str, rows: list[dict[str, object]]) -> None:
    required = REQUIRED_BY_DATASET[dataset]
    for index, row in enumerate(rows, start=1):
        missing = sorted(field for field in required if row.get(field) in {None, ""})
        if missing:
            raise AssertionError(f"{dataset} row {index} missing required CIM fields: {missing}")
        if row.get("cim_data_model") != EXPECTED_MODELS[dataset]:
            raise AssertionError(f"{dataset} row {index} has unexpected cim_data_model={row.get('cim_data_model')!r}")
        if row.get("tag") != EXPECTED_TAGS[dataset]:
            raise AssertionError(f"{dataset} row {index} has unexpected tag={row.get('tag')!r}")


def validate_manifest_counts() -> dict[str, int]:
    manifest = json.loads((DATASET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    return dict(manifest["tables"])


def main() -> None:
    expected_counts = validate_manifest_counts()

    for dataset, path in CSV_FILES.items():
        rows = load_csv(path)
        if len(rows) != expected_counts[dataset]:
            raise AssertionError(f"{dataset} CSV count {len(rows)} != manifest count {expected_counts[dataset]}")
        assert_required_fields(dataset, rows)

    for dataset, path in JSONL_FILES.items():
        rows = load_jsonl(path)
        if len(rows) != expected_counts[dataset]:
            raise AssertionError(f"{dataset} JSONL count {len(rows)} != manifest count {expected_counts[dataset]}")
        for index, row in enumerate(rows, start=1):
            if not row.get("_time") or not row.get("source") or not row.get("table"):
                raise AssertionError(f"{dataset} JSONL row {index} missing _time/source/table")
            if row.get("table") != EXPECTED_JSONL_TABLES[dataset]:
                raise AssertionError(f"{dataset} JSONL row {index} has unexpected table={row.get('table')!r}")
        assert_required_fields(dataset, rows)

    print(f"Validated CIM-friendly ServiceNow demo data: {expected_counts}")


if __name__ == "__main__":
    main()

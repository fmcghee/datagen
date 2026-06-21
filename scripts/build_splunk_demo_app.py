#!/usr/bin/env python3
"""Build and optionally package the ServiceNow ES Demo Splunk app."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "splunk_app" / "demo_servicenow_es"
DATA_DIR = APP_DIR / "bin" / "data"
DIST_DIR = ROOT / "dist"
GENERATOR = ROOT / "scripts" / "generate_servicenow_demo_data.py"

CSV_MAPPINGS = {
    "servicenow_incidents.csv": ROOT / "output" / "servicenow_incidents.csv",
    "servicenow_changes.csv": ROOT / "output" / "servicenow_changes.csv",
    "servicenow_cmdb.csv": ROOT / "output" / "servicenow_cmdb.csv",
    "servicenow_users.csv": ROOT / "output" / "servicenow_users.csv",
    "servicenow_task_ci.csv": ROOT / "datasets" / "servicenow" / "csv" / "servicenow_task_ci.csv",
    "es_incidents.csv": ROOT / "output" / "es_incidents.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the demo_servicenow_es Splunk app.")
    parser.add_argument(
        "--static",
        action="store_true",
        help="Generate fixed-timestamp demo data instead of rolling current dates.",
    )
    parser.add_argument(
        "--package",
        action="store_true",
        help="Create dist/demo_servicenow_es.tar.gz after copying demo data.",
    )
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Copy existing CSV files without regenerating demo data.",
    )
    return parser.parse_args()


def regenerate_demo_data(static: bool) -> None:
    command = [sys.executable, str(GENERATOR)]
    if static:
        command.append("--static")
    else:
        command.extend(["--base-time", "now"])
    subprocess.run(command, check=True, cwd=ROOT)


def copy_demo_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for target_name, source_path in CSV_MAPPINGS.items():
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing demo data file: {source_path}")
        shutil.copy2(source_path, DATA_DIR / target_name)
        print(f"Copied {source_path.name} -> {DATA_DIR / target_name}")


def package_app() -> Path:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = DIST_DIR / "demo_servicenow_es.tar.gz"
    if archive_path.exists():
        archive_path.unlink()

    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(APP_DIR, arcname="demo_servicenow_es")

    print(f"Created {archive_path}")
    return archive_path


def main() -> int:
    args = parse_args()

    if not args.skip_generate:
        regenerate_demo_data(static=args.static)

    copy_demo_data()

    if args.package:
        package_app()

    print(f"App ready at {APP_DIR}")
    print("Install by copying the folder to $SPLUNK_HOME/etc/apps/ and restarting Splunk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

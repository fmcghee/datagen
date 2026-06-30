#!/usr/bin/env python3
"""Convert a Markdown file to DOCX for sharing (e.g. OneDrive)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pypandoc


def convert(source: Path, output: Path | None = None) -> Path:
    if not source.is_file():
        raise FileNotFoundError(f"Source file not found: {source}")

    destination = output or source.with_suffix(".docx")
    destination.parent.mkdir(parents=True, exist_ok=True)

    pypandoc.convert_file(
        str(source),
        to="docx",
        outputfile=str(destination),
        extra_args=["--from=markdown", "--standalone"],
    )
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to the Markdown source file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output DOCX path (default: same name as source with .docx extension)",
    )
    args = parser.parse_args()

    try:
        destination = convert(args.source, args.output)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Create non-destructive mobile-app blueprint documents from bundled templates."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys


DOCUMENTS = {
    "APP-PLAN.md": "APP-PLAN.md",
    "ARCHITECTURE.md": "ARCHITECTURE.md",
    "TECH-STACK.md": "TECH-STACK.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create APP-PLAN.md, ARCHITECTURE.md, and TECH-STACK.md."
    )
    parser.add_argument("--app-name", required=True, help="Human-readable app name")
    parser.add_argument("--platform", required=True, help="Target platform, such as iOS 17+")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs"),
        help="Destination directory (default: docs)",
    )
    parser.add_argument(
        "--status",
        choices=("Proposed", "Confirmed"),
        default="Proposed",
        help="Initial document status (default: Proposed)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the three destination files if they already exist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.app_name.strip() or not args.platform.strip():
        print("App name and platform must not be blank.", file=sys.stderr)
        return 2

    template_dir = Path(__file__).resolve().parent.parent / "assets" / "templates"
    destinations = {name: args.output / name for name in DOCUMENTS}

    missing_templates = [
        str(template_dir / template)
        for template in DOCUMENTS.values()
        if not (template_dir / template).is_file()
    ]
    if missing_templates:
        print("Missing template files:", file=sys.stderr)
        for path in missing_templates:
            print(f"  {path}", file=sys.stderr)
        return 2

    conflicts = [str(path) for path in destinations.values() if path.exists()]
    if conflicts and not args.force:
        print("Refusing to overwrite existing files:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        print("Re-run with --force only when replacement is intended.", file=sys.stderr)
        return 1

    replacements = {
        "{{APP_NAME}}": args.app_name.strip(),
        "{{PLATFORM}}": args.platform.strip(),
        "{{DATE}}": date.today().isoformat(),
        "{{STATUS}}": args.status,
    }

    args.output.mkdir(parents=True, exist_ok=True)
    for destination_name, template_name in DOCUMENTS.items():
        content = (template_dir / template_name).read_text(encoding="utf-8")
        for token, value in replacements.items():
            content = content.replace(token, value)
        destination = destinations[destination_name]
        destination.write_text(content, encoding="utf-8", newline="\n")
        print(destination)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

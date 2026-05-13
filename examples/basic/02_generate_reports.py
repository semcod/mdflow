#!/usr/bin/env python3
"""
Example: Generate HTML, Markdown and Mermaid reports for a single file.

Run from project root:
    python examples/basic/02_generate_reports.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def main():
    flow = MdFlow()
    doc = flow.parse("examples/data/project_overview.md")

    # Generate all report formats
    output_dir = "examples/output/basic"
    written = flow.report(doc, output_dir, formats=["html", "md", "mermaid"])

    print(f"Generated {len(written)} files in {output_dir}/:")
    for path in written:
        size = path.stat().st_size
        print(f"  {path.name:40s} ({size:,} bytes)")

    # Generate only HTML this time
    print("\n--- HTML only ---")
    written_html = flow.report(doc, output_dir, formats=["html"])
    for path in written_html:
        print(f"  {path.name}")


if __name__ == "__main__":
    main()

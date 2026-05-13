#!/usr/bin/env python3
"""
Example: Parse a single Markdown file and inspect its structure.

Run from project root:
    python examples/basic/01_parse_single_file.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def main():
    flow = MdFlow()

    # Parse a single file
    doc = flow.parse("examples/data/project_overview.md")

    print("=" * 60)
    print(f"Title : {doc.title}")
    print(f"Path  : {doc.path}")
    print("=" * 60)

    # Document statistics
    print(f"\nHeadings      : {len(doc.headings)}")
    print(f"Code blocks   : {len(doc.code_blocks)}")
    print(f"Links         : {len(doc.links)}")
    print(f"  - Internal  : {len(doc.internal_links)}")
    print(f"  - External  : {len(doc.external_links)}")
    print(f"  - Anchors   : {len(doc.anchor_links)}")
    print(f"List items    : {len(doc.list_items)}")
    print(f"TOON sections : {len(doc.toon_sections)}")
    print(f"Markpact refs : {len(doc.markpact_blocks)}")

    # Show heading hierarchy
    print("\n--- Heading hierarchy ---")
    for h in doc.headings:
        indent = "  " * (h.level - 1)
        print(f"{indent}{h.level}. {h.text}  (line {h.line})")

    # Show metadata if present
    if doc.metadata:
        print("\n--- Metadata ---")
        for key, value in doc.metadata.items():
            print(f"  {key:15s}: {value}")

    # Show first 3 list items
    if doc.list_items:
        print("\n--- First list items ---")
        for li in doc.list_items[:3]:
            indent = "  " * li.depth
            print(f"{indent}- {li.text}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Basic usage example for mdflow.

This example demonstrates how to:
- Parse a single Markdown file
- Access basic document properties
- Generate reports

Run:
    python examples/basic_usage.py
"""
import sys
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from mdflow import MdFlow


def main():
    # Initialize mdflow
    flow = MdFlow()

    # Parse a Markdown file
    # Change this path to your actual .md file
    doc_path = "../SUMR.md"
    doc = flow.parse(doc_path)

    print("=" * 60)
    print("Basic Document Information")
    print("=" * 60)
    print(f"Title:           {doc.title}")
    print(f"Path:            {doc.path}")
    print(f"Headings:        {len(doc.headings)}")
    print(f"Code blocks:     {len(doc.code_blocks)}")
    print(f"Links:           {len(doc.links)}")
    print(f"  - Internal:    {len(doc.internal_links)}")
    print(f"  - External:    {len(doc.external_links)}")
    print(f"  - Anchors:     {len(doc.anchor_links)}")
    print(f"List items:      {len(doc.list_items)}")
    print(f"TOON sections:   {len(doc.toon_sections)}")
    print(f"Markpact blocks: {len(doc.markpact_blocks)}")
    print("=" * 60)

    # Access headings
    print("\nTop-level headings:")
    for h in doc.headings[:5]:
        indent = "  " * (h.level - 1)
        print(f"{indent}- {h.text} (line {h.line})")

    # Access metadata if present
    if doc.metadata:
        print("\nDocument metadata:")
        for key, value in doc.metadata.items():
            print(f"  {key}: {value}")

    # Generate reports
    print("\nGenerating reports...")
    output_dir = "../output"
    written = flow.report(doc, output_dir, formats=["html", "md"])
    print(f"\nWritten {len(written)} files to {output_dir}/")


if __name__ == "__main__":
    main()

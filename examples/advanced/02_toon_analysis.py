#!/usr/bin/env python3
"""
Example: Extract and analyze TOON quality metrics.

TOON sections (in toon/yaml code blocks or markpact:analysis blocks)
carry structured quality data like HEALTH, ALERTS, REFACTOR tasks, etc.

Run from project root:
    python examples/advanced/02_toon_analysis.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def main():
    flow = MdFlow()

    # Parse a file that contains TOON data
    doc = flow.parse("examples/data/deployment.md")

    print(f"Document: {doc.title}")
    print(f"TOON sections found: {[ts.name for ts in doc.toon_sections]}")

    # Extract TOON metrics
    metrics = flow.toon_metrics(doc)

    print("\n" + "=" * 60)
    print("TOON Metrics")
    print("=" * 60)

    for category in ["health", "alerts", "refactors", "risks", "hotspots"]:
        data = metrics.get(category)
        if not data:
            continue

        print(f"\n--- {category.upper()} ---")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  {key:20s}: {value}")
        elif isinstance(data, list):
            for item in data[:5]:
                print(f"  - {item}")
            if len(data) > 5:
                print(f"  ... and {len(data) - 5} more")

    # Show raw TOON sections
    if doc.toon_sections:
        print("\n--- Raw TOON sections ---")
        for ts in doc.toon_sections:
            print(f"\n{ts.name}:")
            for item in ts.items[:5]:
                print(f"  - {item}")
            if len(ts.items) > 5:
                print(f"  ... and {len(ts.items) - 5} more items")


if __name__ == "__main__":
    main()

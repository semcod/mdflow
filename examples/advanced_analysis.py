#!/usr/bin/env python3
"""
Advanced analysis example for mdflow.

This example demonstrates how to:
- Use built-in analyzers (structure, code inventory, TOON metrics)
- Access detailed analysis results
- Work with markpact embedded file references

Run:
    python examples/advanced_analysis.py
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
    doc_path = "../SUMR.md"
    doc = flow.parse(doc_path)

    print("=" * 60)
    print("Structure Analysis")
    print("=" * 60)
    
    # Get structure analysis
    structure = flow.structure(doc)
    
    print("\nHeading tree:")
    print(structure["heading_tree"])
    
    print("\nSection summary:")
    for section in structure["sections"][:5]:
        print(f"  - {section}")

    print("\n" + "=" * 60)
    print("Code Inventory Analysis")
    print("=" * 60)
    
    # Get code inventory
    inventory = flow.code_inventory(doc)
    
    print(f"\nTotal code blocks: {inventory.get('total', 0)}")
    print("\nCode blocks by language:")
    for lang, count in inventory.get("by_language", {}).items():
        print(f"  {lang:15s}: {count}")

    print("\nMarkpact embedded references:")
    for ref in inventory.get("markpact_refs", []):
        print(f"  - markpact:{ref['type']} path={ref['path']}")

    print("\n" + "=" * 60)
    print("TOON Quality Metrics")
    print("=" * 60)
    
    # Get TOON metrics
    metrics = flow.toon_metrics(doc)
    
    if metrics.get("health"):
        print("\nHealth metrics:")
        for key, value in metrics["health"].items():
            print(f"  {key}: {value}")
    
    if metrics.get("alerts"):
        print(f"\nAlerts ({len(metrics['alerts'])} total):")
        for alert in metrics["alerts"][:5]:
            print(f"  - {alert}")
        if len(metrics["alerts"]) > 5:
            print(f"  ... and {len(metrics['alerts']) - 5} more")
    
    if metrics.get("refactors"):
        print(f"\nRefactor tasks ({len(metrics['refactors'])} total):")
        for task in metrics["refactors"][:5]:
            print(f"  - {task}")
        if len(metrics["refactors"]) > 5:
            print(f"  ... and {len(metrics['refactors']) - 5} more")
    
    if metrics.get("risks"):
        print(f"\nRisks ({len(metrics['risks'])} total):")
        for risk in metrics["risks"][:5]:
            print(f"  - {risk}")

    print("\n" + "=" * 60)
    print("TOON Sections Found")
    print("=" * 60)
    
    for ts in doc.toon_sections:
        print(f"\n{ts.name}:")
        for item in ts.items[:3]:
            print(f"  - {item}")
        if len(ts.items) > 3:
            print(f"  ... and {len(ts.items) - 3} more items")


if __name__ == "__main__":
    main()

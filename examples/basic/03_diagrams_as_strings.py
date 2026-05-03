#!/usr/bin/env python3
"""
Example: Get Mermaid diagrams as strings (no files written).

Useful for embedding diagrams in other tools or custom templates.

Run from project root:
    python examples/basic/03_diagrams_as_strings.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def main():
    flow = MdFlow()
    doc = flow.parse("examples/data/project_overview.md")

    # Get all diagrams as strings
    diagrams = flow.diagrams(doc)

    print("Available diagrams:\n")
    for name, code in diagrams.items():
        lines = code.count("\n") + 1 if code else 0
        status = f"{lines} lines" if code else "empty (no data)"
        print(f"  {name:25s}: {status}")

    # Print a specific diagram to stdout
    print("\n" + "=" * 60)
    print("Section flowchart (first 15 lines):")
    print("=" * 60)
    if diagrams.get("section_flow"):
        for line in diagrams["section_flow"].splitlines()[:15]:
            print(line)
        if diagrams["section_flow"].count("\n") > 15:
            print("  ...")


if __name__ == "__main__":
    main()

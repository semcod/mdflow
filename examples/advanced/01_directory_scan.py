#!/usr/bin/env python3
"""
Example: Scan an entire directory of Markdown files.

Builds cross-document dependency graphs and generates per-file reports.

Run from project root:
    python examples/advanced/01_directory_scan.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def main():
    flow = MdFlow()

    # Scan the data directory
    docs, graph = flow.scan(
        "examples/data",
        output_dir="examples/output/advanced/scan",
        formats=["html", "md", "mermaid"],
    )

    print(f"\nParsed {len(docs)} documents")
    print(f"Dependency graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    # List all documents found
    print("\n--- Documents ---")
    for doc in docs:
        print(
            f"  {Path(doc.path).name:30s}  "
            f"{len(doc.headings):3d} headings  "
            f"{len(doc.links):3d} links  "
            f"{len(doc.code_blocks):3d} code blocks"
        )

    # Show dependency edges
    if graph.edges:
        print("\n--- Cross-document dependencies ---")
        for edge in graph.edges:
            print(f"  {edge.source} --[{edge.kind}]--> {edge.target}")


if __name__ == "__main__":
    main()

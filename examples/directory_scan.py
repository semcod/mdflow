#!/usr/bin/env python3
"""
Directory scan example for mdflow.

This example demonstrates how to:
- Scan an entire directory of Markdown files
- Generate reports for all files
- Build cross-document dependency graphs

Run:
    python examples/directory_scan.py
"""
import sys
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from mdflow import MdFlow


def main():
    # Initialize mdflow
    flow = MdFlow()

    # Scan a directory (change this to your actual directory)
    root_dir = "../mdflow"  # scanning the mdflow source directory
    output_dir = "../output/scan"

    print("=" * 60)
    print(f"Scanning directory: {root_dir}")
    print("=" * 60)

    # Parse all .md files in the directory
    docs = flow.parse_dir(root_dir)
    print(f"\nFound {len(docs)} Markdown files:")
    for doc in docs:
        print(f"  - {doc.path} ({doc.title})")

    # Build dependency graph
    print("\n" + "=" * 60)
    print("Building Dependency Graph")
    print("=" * 60)
    
    graph = flow.dependency_graph(docs)
    print(f"\nNodes (documents): {len(graph.nodes)}")
    print(f"Edges (dependencies): {len(graph.edges)}")
    
    if graph.edges:
        print("\nDependency edges:")
        for edge in graph.edges[:10]:
            print(f"  {edge.source} -> {edge.target} ({edge.kind})")
        if len(graph.edges) > 10:
            print(f"  ... and {len(graph.edges) - 10} more edges")

    # Generate reports for all files
    print("\n" + "=" * 60)
    print("Generating Reports")
    print("=" * 60)
    
    docs, graph = flow.scan(root_dir, output_dir, formats=["html", "md"])
    print(f"\nGenerated reports for {len(docs)} documents in {output_dir}/")

    # Analyze individual documents
    print("\n" + "=" * 60)
    print("Document Summary")
    print("=" * 60)
    
    for doc in docs:
        print(f"\n{doc.title}:")
        print(f"  Headings: {len(doc.headings)}")
        print(f"  Code blocks: {len(doc.code_blocks)}")
        print(f"  Links: {len(doc.links)}")
        if doc.toon_sections:
            print(f"  TOON sections: {', '.join(ts.name for ts in doc.toon_sections)}")


if __name__ == "__main__":
    main()

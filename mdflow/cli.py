#!/usr/bin/env python3
"""
mdflow CLI — analyze Markdown files and generate dependency diagrams.

Usage:
    python -m mdflow.cli analyze SUMR.md --output output/
    python -m mdflow.cli scan docs/ --output output/
    python -m mdflow.cli diagram SUMR.md --diagram section_flow
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from . import MdFlow


def cmd_analyze(args):
    flow = MdFlow()
    doc = flow.parse(args.file)
    print(f"[mdflow] Parsed: {doc.title}")
    print(f"  Headings:    {len(doc.headings)}")
    print(f"  Code blocks: {len(doc.code_blocks)}")
    print(f"  Links:       {len(doc.links)} "
          f"({len(doc.internal_links)} internal, {len(doc.external_links)} external)")
    print(f"  Markpact:    {len(doc.markpact_blocks)}")
    print(f"  TOON secs:   {', '.join(ts.name for ts in doc.toon_sections) or '—'}")

    formats = args.format.split(",") if args.format else ["html", "md", "mermaid"]
    flow.report(doc, args.output, formats=formats)


def cmd_scan(args):
    flow = MdFlow()
    formats = args.format.split(",") if args.format else ["html", "md", "mermaid"]
    docs, graph = flow.scan(args.dir, args.output, formats=formats)
    print(f"[mdflow] Done. {len(docs)} files, {len(graph.edges)} dependency edges.")


def cmd_diagram(args):
    flow = MdFlow()
    doc = flow.parse(args.file)
    diagrams = flow.diagrams(doc)
    name = args.diagram

    if name == "list":
        print("Available diagrams:", ", ".join(diagrams.keys()))
        return

    if name not in diagrams:
        print(f"Unknown diagram '{name}'. Use 'list' to see options.")
        sys.exit(1)

    diagram = diagrams[name]
    if not diagram:
        print(f"No {name} diagram generated (nothing to show).")
        return

    if args.output:
        p = Path(args.output)
        p.write_text(diagram, encoding="utf-8")
        print(f"[mdflow] Written: {p}")
    else:
        print(diagram)


def main():
    parser = argparse.ArgumentParser(
        prog="mdflow",
        description="Markdown dependency analyzer and diagram generator"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = sub.add_parser("analyze", help="Analyze a single Markdown file")
    p_analyze.add_argument("file", help="Path to .md file")
    p_analyze.add_argument("-o", "--output", default="output", help="Output directory")
    p_analyze.add_argument("--format", help="Comma-separated: html,md,mermaid")
    p_analyze.set_defaults(func=cmd_analyze)

    # scan
    p_scan = sub.add_parser("scan", help="Scan a directory of Markdown files")
    p_scan.add_argument("dir", help="Root directory to scan")
    p_scan.add_argument("-o", "--output", default="output", help="Output directory")
    p_scan.add_argument("--format", help="Comma-separated: html,md,mermaid")
    p_scan.set_defaults(func=cmd_scan)

    # diagram
    p_diag = sub.add_parser("diagram", help="Print a single Mermaid diagram")
    p_diag.add_argument("file", help="Path to .md file")
    p_diag.add_argument("--diagram", default="section_flow",
                        help="Diagram name (or 'list' to see all)")
    p_diag.add_argument("-o", "--output", help="Write diagram to file instead of stdout")
    p_diag.set_defaults(func=cmd_diagram)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

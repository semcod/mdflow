"""
Analyze prefact project documentation with mdflow.

Demonstrates: parsing SUMD.md from a real semcod project,
extracting TOON quality metrics, and generating a cross-section report.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mdflow import MdFlow

PREFACT_ROOT = Path("/home/tom/github/semcod/prefact")
OUT = Path("/tmp/mdflow_prefact_out")

flow = MdFlow()

doc = flow.parse(PREFACT_ROOT / "SUMD.md")

print(f"Project : prefact")
print(f"Headings: {len(doc.headings)}")
print(f"Code blocks: {len(doc.code_blocks)}")
print(f"Links   : {len(doc.links)}")
print(f"TOON    : {[ts.name for ts in doc.toon_sections]}")

diagrams = flow.diagrams(doc)
print(f"\nDiagrams available: {list(diagrams.keys())}")
for name, content in diagrams.items():
    if content:
        print(f"  {name}: {len(content.splitlines())} lines")

flow.report(doc, OUT, formats=["md", "mermaid"])
print(f"\nReports written to {OUT}/")

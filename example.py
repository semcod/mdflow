#!/usr/bin/env python3
"""
example.py — demonstrate mdflow against the uploaded SUMR.md file.

Run:
    python example.py
"""

import sys
from pathlib import Path

# allow running from the mdflow directory without install
sys.path.insert(0, str(Path(__file__).parent))

from mdflow import MdFlow

# ── parse ─────────────────────────────────────────────────────────────────────
flow = MdFlow()
doc = flow.parse("SUMR.md")

print("=" * 60)
print(f"Document  : {doc.title}")
print(f"Path      : {doc.path}")
print(f"Headings  : {len(doc.headings)}")
print(f"Code blks : {len(doc.code_blocks)}")
print(f"Links     : {len(doc.links)}")
print(f"List items: {len(doc.list_items)}")
print(f"TOON secs : {[ts.name for ts in doc.toon_sections]}")
print(f"Markpact  : {[cb.markpact_type for cb in doc.markpact_blocks]}")
print("=" * 60)

# ── metadata ─────────────────────────────────────────────────────────────────
if doc.metadata:
    print("\n📋 Metadata")
    for k, v in doc.metadata.items():
        print(f"  {k:20s}: {v}")

# ── toon metrics ─────────────────────────────────────────────────────────────
metrics = flow.toon_metrics(doc)
if metrics["health"]:
    print("\n🔬 Health")
    for k, v in metrics["health"].items():
        print(f"  {k}: {v}")

if metrics["alerts"]:
    print(f"\n⚠  Alerts ({len(metrics['alerts'])})")
    for a in metrics["alerts"][:5]:
        print(f"  {a}")

if metrics["refactors"]:
    print(f"\n🔧 Refactors ({len(metrics['refactors'])})")
    for r in metrics["refactors"][:5]:
        print(f"  {r}")

# ── diagrams ──────────────────────────────────────────────────────────────────
print("\n📐 Diagrams available:")
diags = flow.diagrams(doc)
for name, code in diags.items():
    lines = code.count("\n") + 1 if code else 0
    status = f"{lines} lines" if code else "—"
    print(f"  {name:25s}: {status}")

# ── generate reports ─────────────────────────────────────────────────────────
print("\n📁 Generating reports → output/")
written = flow.report(doc, "output", formats=["html", "md", "mermaid"])
print(f"Written {len(written)} files.")

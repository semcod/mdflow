"""
Scan multiple semcod projects and produce a cross-project summary.

Demonstrates: multi-project scan, dependency graph across repos,
aggregating TOON health metrics from all SUMD.md files.
"""

from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mdflow import MdFlow

SEMCOD = Path("/home/tom/github/semcod")
PROJECTS = ["prefact", "pyqual", "planfile", "goal", "costs", "pfix"]
OUT = Path("/tmp/mdflow_workspace_scan")

flow = MdFlow()

all_docs = []
for project in PROJECTS:
    sumd = SEMCOD / project / "SUMD.md"
    if sumd.exists():
        doc = flow.parse(sumd)
        all_docs.append((project, doc))
        print(
            f"[{project}] headings={len(doc.headings)} code={len(doc.code_blocks)} toon={len(doc.toon_sections)}"
        )

print(f"\nTotal projects parsed: {len(all_docs)}")

graph = flow.dependency_graph([doc for _, doc in all_docs])
print(f"Dependency graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

print("\n--- TOON health summary ---")
for project, doc in all_docs:
    metrics = flow._toon.metrics(doc)
    health = metrics.get("health", {})
    alerts = metrics.get("alerts", [])
    refactors = metrics.get("refactors", [])
    cc = health.get("cc_mean", "n/a")
    print(
        f"  {project:12s} CC={cc:>4}  alerts={len(alerts)}  refactors={len(refactors)}"
    )

OUT.mkdir(parents=True, exist_ok=True)
for project, doc in all_docs:
    proj_out = OUT / project
    flow.report(doc, proj_out, formats=["md"])
    print(f"[{project}] → {proj_out}/")

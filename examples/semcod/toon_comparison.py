"""
Compare TOON quality metrics across semcod projects.

Demonstrates: extracting structured TOON data from SUMR.md files
(which contain actual CC, coverage, and refactor analysis),
ranking projects by complexity.
"""

from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from mdflow import MdFlow

SEMCOD = Path("/home/tom/github/semcod")
PROJECTS = ["prefact", "pyqual", "planfile", "goal", "mdflow"]

flow = MdFlow()

rows = []
for project in PROJECTS:
    for fname in ("SUMR.md", "SUMD.md"):
        md_path = SEMCOD / project / fname
        if md_path.exists():
            doc = flow.parse(md_path)
            metrics = flow._toon.metrics(doc)
            rows.append(
                {
                    "project": project,
                    "file": fname,
                    "cc_mean": metrics["health"].get("cc_mean", "—"),
                    "critical": metrics["health"].get("critical", "—"),
                    "alerts": len(metrics["alerts"]),
                    "refactors": len(metrics["refactors"]),
                    "toon_secs": ", ".join(metrics["toon_sections"]) or "—",
                }
            )
            break

header = f"{'Project':<12} {'File':<8} {'CC̄':>5} {'Crit':>5} {'Alerts':>7} {'Refactors':>10}  TOON sections"
print(header)
print("-" * len(header))
for r in sorted(rows, key=lambda x: str(x["cc_mean"]), reverse=True):
    print(
        f"{r['project']:<12} {r['file']:<8} {str(r['cc_mean']):>5} "
        f"{str(r['critical']):>5} {r['alerts']:>7} {r['refactors']:>10}  {r['toon_secs']}"
    )

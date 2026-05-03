"""Helper script for testql scenario 06 — validate mermaid files in a directory.

Usage:
  python3 _validate_mermaid.py <dir>           — full validation
  python3 _validate_mermaid.py <dir> --pie-check — check pie title format only
"""
import sys
from pathlib import Path

sys.path.insert(0, "/home/tom/github/semcod/mdflow")
from mdflow.validators import validate_mermaid_files

target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/tq_mermaid_val")

if "--pie-check" in sys.argv:
    pie = target / "SUMD_code_pie.mermaid"
    if not pie.exists():
        print("PIE_MISSING")
        sys.exit(0)
    first = pie.read_text().splitlines()[0].strip()
    if first.startswith("pie title ") and not first.startswith('pie title "'):
        print("PIE_OK")
        sys.exit(0)
    print(f"PIE_BAD: {first}")
    sys.exit(1)

files = list(target.glob("*.mermaid"))
results = validate_mermaid_files(files)
errors = [r for r in results if not r.valid]
print(f"VALIDATED files={len(files)} errors={len(errors)}")
for e in errors:
    for i in e.issues:
        if i.severity == "error":
            print(f"  ERROR {i.code} in {e.diagram_name}: {i.message}")
sys.exit(len(errors))

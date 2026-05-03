#!/bin/bash
# CLI examples — analyzing real semcod/* projects with mdflow
# Run from: /home/tom/github/semcod/mdflow/

set -euo pipefail
MDFLOW="python3 -m mdflow.cli"
SEMCOD="/home/tom/github/semcod"
OUT="/tmp/mdflow_cli_semcod"

echo "=== mdflow CLI — semcod workspace examples ==="
mkdir -p "$OUT"

# 1. Analyze prefact SUMD.md (Markdown + Mermaid diagrams only)
echo ""
echo "--- [1] prefact/SUMD.md → md + mermaid"
$MDFLOW analyze "$SEMCOD/prefact/SUMD.md" \
    --output "$OUT/prefact" \
    --format md,mermaid

# 2. Analyze pyqual SUMD.md (HTML report)
echo ""
echo "--- [2] pyqual/SUMD.md → html"
$MDFLOW analyze "$SEMCOD/pyqual/SUMD.md" \
    --output "$OUT/pyqual" \
    --format html

# 3. Analyze planfile SUMR.md — all formats
echo ""
echo "--- [3] planfile/SUMR.md → all formats"
$MDFLOW analyze "$SEMCOD/planfile/SUMR.md" \
    --output "$OUT/planfile" \
    --format html,md,mermaid

# 4. Print section flow diagram for goal/README.md to stdout
echo ""
echo "--- [4] goal/README.md section_flow (stdout)"
$MDFLOW diagram "$SEMCOD/goal/README.md" --diagram section_flow

# 5. Print heading mindmap for costs/README.md to stdout
echo ""
echo "--- [5] costs/README.md heading_mindmap (stdout)"
$MDFLOW diagram "$SEMCOD/costs/README.md" --diagram heading_mindmap

# 6. Save section_flow diagram to file
echo ""
echo "--- [6] prefact/README.md section_flow → file"
$MDFLOW diagram "$SEMCOD/prefact/README.md" \
    --diagram section_flow \
    -o "$OUT/prefact_section_flow.mermaid"
echo "Saved: $OUT/prefact_section_flow.mermaid"

# 7. Scan entire planfile docs directory
echo ""
echo "--- [7] scan planfile/docs/ → md reports"
if [ -d "$SEMCOD/planfile/docs" ]; then
    $MDFLOW scan "$SEMCOD/planfile/docs/" \
        --output "$OUT/planfile_docs_scan" \
        --format md
else
    echo "  (planfile/docs/ not found, skipping)"
fi

# 8. Scan prefact docs/ directory
echo ""
echo "--- [8] scan prefact/docs/ → md reports"
$MDFLOW scan "$SEMCOD/prefact/docs/" \
    --output "$OUT/prefact_docs_scan" \
    --format md

echo ""
echo "=== Done. Output in: $OUT ==="
ls "$OUT/"

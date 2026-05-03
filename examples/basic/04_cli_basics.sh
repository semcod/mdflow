#!/bin/bash
# Example: Basic CLI usage of mdflow.
#
# Run from project root:
#     bash examples/basic/04_cli_basics.sh

set -e

echo "=== mdflow CLI Examples ==="
echo ""

# Analyze a single file (all formats)
echo "--- 1. Analyze single file (all formats) ---"
python -m mdflow.cli analyze examples/data/project_overview.md --output examples/output/cli

# Analyze with selected formats
echo ""
echo "--- 2. Analyze with HTML + Markdown only ---"
python -m mdflow.cli analyze examples/data/api_reference.md --output examples/output/cli --format html,md

# List available diagrams
echo ""
echo "--- 3. List available diagrams ---"
python -m mdflow.cli diagram examples/data/project_overview.md --diagram list

# Extract a specific diagram to stdout
echo ""
echo "--- 4. Print section_flow diagram to stdout ---"
python -m mdflow.cli diagram examples/data/project_overview.md --diagram section_flow | head -20

# Save a diagram to file
echo ""
echo "--- 5. Save heading_mindmap to file ---"
python -m mdflow.cli diagram examples/data/project_overview.md --diagram heading_mindmap -o examples/output/cli/heading_mindmap.mermaid

echo ""
echo "=== Done. Check examples/output/cli/ for results ==="

#!/bin/bash
# CLI usage examples for mdflow
# 
# This script demonstrates various ways to use the mdflow CLI
# Make sure mdflow is installed first: pip install -e .
#
# Run:
#   bash examples/cli_usage.sh

echo "=========================================="
echo "mdflow CLI Usage Examples"
echo "=========================================="
echo ""

# Example 1: Analyze a single file
echo "1. Analyze a single Markdown file:"
echo "   mdflow analyze SUMR.md --output output/"
echo ""

# Example 2: Select specific output formats
echo "2. Generate only HTML and Markdown reports:"
echo "   mdflow analyze SUMR.md --format html,md --output output/"
echo ""

# Example 3: Generate only Mermaid diagrams
echo "3. Generate only Mermaid diagrams:"
echo "   mdflow analyze SUMR.md --format mermaid --output output/"
echo ""

# Example 4: Scan a directory
echo "4. Scan an entire directory of Markdown files:"
echo "   mdflow scan docs/ --output output/scan"
echo ""

# Example 5: List available diagrams
echo "5. List available diagram types:"
echo "   mdflow diagram SUMR.md --diagram list"
echo ""

# Example 6: Print a specific diagram to stdout
echo "6. Print section flow diagram to stdout:"
echo "   mdflow diagram SUMR.md --diagram section_flow"
echo ""

# Example 7: Save a specific diagram to file
echo "7. Save a specific diagram to file:"
echo "   mdflow diagram SUMR.md --diagram alerts_graph -o alerts.mermaid"
echo ""

# Example 8: Scan with specific formats
echo "8. Scan directory with specific formats:"
echo "   mdflow scan docs/ --format html,md --output output/scan"
echo ""

echo "=========================================="
echo "Running actual examples..."
echo "=========================================="
echo ""

# Check if SUMR.md exists
if [ -f "../SUMR.md" ]; then
    echo "Analyzing SUMR.md..."
    cd ..
    mdflow analyze SUMR.md --output output/
    echo ""
    echo "Done! Check the output/ directory for generated files."
else
    echo "SUMR.md not found. Skipping actual examples."
    echo "Create a SUMR.md file or update the path in this script."
fi

#!/usr/bin/env python3
"""
Custom diagrams example for mdflow.

This example demonstrates how to:
- Generate diagrams as strings without writing files
- Access individual diagram types
- Embed diagrams in custom outputs

Run:
    python examples/custom_diagrams.py
"""
import sys
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from mdflow import MdFlow


def main():
    # Initialize mdflow
    flow = MdFlow()

    # Parse a Markdown file
    doc_path = "../SUMR.md"
    doc = flow.parse(doc_path)

    print("=" * 60)
    print("Available Diagrams")
    print("=" * 60)

    # Get all diagrams as strings (no files written)
    diagrams = flow.diagrams(doc)
    
    for name, diagram in diagrams.items():
        lines = diagram.count("\n") + 1 if diagram else 0
        status = f"{lines} lines" if diagram else "— (empty)"
        print(f"  {name:25s}: {status}")

    print("\n" + "=" * 60)
    print("Section Flow Diagram")
    print("=" * 60)
    print(diagrams.get("section_flow", "No diagram available"))

    print("\n" + "=" * 60)
    print("Heading Mindmap Diagram")
    print("=" * 60)
    print(diagrams.get("heading_mindmap", "No diagram available"))

    print("\n" + "=" * 60)
    print("Code Inventory Pie Chart")
    print("=" * 60)
    print(diagrams.get("code_pie", "No diagram available"))

    # Example: Save a specific diagram to a custom file
    print("\n" + "=" * 60)
    print("Saving Custom Diagram")
    print("=" * 60)
    
    if diagrams.get("alerts_graph"):
        custom_path = "../output/custom_alerts.mermaid"
        Path(custom_path).parent.mkdir(parents=True, exist_ok=True)
        Path(custom_path).write_text(diagrams["alerts_graph"], encoding="utf-8")
        print(f"Saved alerts_graph to {custom_path}")

    # Example: Embed diagram in custom HTML
    print("\n" + "=" * 60)
    print("Custom HTML Output Example")
    print("=" * 60)
    
    if diagrams.get("section_flow"):
        custom_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Custom Report</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <h1>Custom Report: {doc.title}</h1>
    <h2>Section Flow</h2>
    <pre class="mermaid">
{diagrams["section_flow"]}
    </pre>
</body>
</html>"""
        custom_html_path = "../output/custom_report.html"
        Path(custom_html_path).write_text(custom_html, encoding="utf-8")
        print(f"Saved custom HTML report to {custom_html_path}")


if __name__ == "__main__":
    main()

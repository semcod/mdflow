#!/usr/bin/env python3
"""
Example: Build a custom diagram pipeline.

Instead of using the high-level MdFlow.report(), we manually:
1. Parse documents
2. Extract specific data
3. Generate only selected diagrams
4. Embed them in a custom HTML template

Run from project root:
    python examples/advanced/03_custom_diagram_pipeline.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow
from mdflow.generators import mermaid as mm


def main():
    flow = MdFlow()

    # Parse multiple files
    files = [
        "examples/data/project_overview.md",
        "examples/data/api_reference.md",
        "examples/data/deployment.md",
    ]

    docs = [flow.parse(f) for f in files]

    # Build a custom page with all heading mindmaps
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='UTF-8'>",
        "<title>Custom Diagram Pipeline</title>",
        "<script src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>",
        "</head><body>",
        "<h1>Heading Mindmaps</h1>",
    ]

    for doc in docs:
        tree = flow.structure(doc)["heading_tree"]
        diagram = mm.heading_tree_diagram(tree, doc.title)

        if diagram:
            html_parts.append(f"<h2>{doc.title}</h2>")
            html_parts.append("<pre class='mermaid'>")
            html_parts.append(diagram)
            html_parts.append("</pre>")

    html_parts += [
        "<script>mermaid.initialize({startOnLoad:true})</script>",
        "</body></html>",
    ]

    # Write custom output
    out_path = Path("examples/output/advanced/custom_pipeline.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(html_parts), encoding="utf-8")

    print(f"Custom HTML written to: {out_path}")
    print(f"  Documents processed: {len(docs)}")
    print(f"  Total size: {out_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

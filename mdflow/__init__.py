"""
mdflow — Markdown dependency analyzer and diagram generator.

Usage:
    from mdflow import MdFlow

    flow = MdFlow()
    doc  = flow.parse("SUMR.md")
    flow.report(doc, "output/")      # → HTML + Markdown + diagrams
    flow.scan("docs/", "output/")    # → scan entire directory
"""

from __future__ import annotations
from pathlib import Path
from .models import MdDocument, DependencyGraph
from .parser import MdParser
from .analyzers import (
    DependencyAnalyzer,
    StructureAnalyzer,
    CodeInventoryAnalyzer,
    ToonAnalyzer,
)
from .generators import generate_html_report, generate_markdown_report
from .generators import mermaid as mm

__version__ = "0.1.5"
__all__ = ["MdFlow", "MdParser", "MdDocument", "DependencyGraph"]


class MdFlow:
    """
    High-level façade for the mdflow library.

    Examples
    --------
    Single file:
        flow = MdFlow()
        doc  = flow.parse("SUMR.md")
        flow.report(doc, "output/")

    Directory scan:
        flow = MdFlow()
        flow.scan("docs/", "output/")
    """

    def __init__(self):
        self._parser = MdParser()
        self._dep = DependencyAnalyzer()
        self._struct = StructureAnalyzer()
        self._code_inv = CodeInventoryAnalyzer()
        self._toon = ToonAnalyzer()

    # ── parsing ───────────────────────────────────────────────────────────────

    def parse(self, path: str | Path) -> MdDocument:
        """Parse a single Markdown file into an MdDocument."""
        return self._parser.parse(Path(path))

    def parse_dir(self, root: str | Path) -> list[MdDocument]:
        """Parse all .md files in a directory tree."""
        root = Path(root)
        docs = []
        for p in sorted(root.rglob("*.md")):
            try:
                docs.append(self._parser.parse(p))
            except Exception as e:
                print(f"[mdflow] warning: could not parse {p}: {e}")
        return docs

    # ── analysis ──────────────────────────────────────────────────────────────

    def dependency_graph(self, docs: list[MdDocument]) -> DependencyGraph:
        """Build a cross-document dependency graph."""
        return self._dep.build(docs)

    def structure(self, doc: MdDocument) -> dict:
        """Return heading tree + section summary for one document."""
        return {
            "heading_tree": self._struct.heading_tree(doc),
            "sections": self._struct.section_summary(doc),
        }

    def code_inventory(self, doc: MdDocument) -> dict:
        """Return code block inventory for one document."""
        return self._code_inv.inventory(doc)

    def toon_metrics(self, doc: MdDocument) -> dict:
        """Extract TOON quality metrics from one document."""
        return self._toon.metrics(doc)

    # ── report generation ─────────────────────────────────────────────────────

    def report(
        self,
        doc: MdDocument,
        output_dir: str | Path = ".",
        formats: list[str] | None = None,
    ):
        """
        Generate reports for a single document.

        formats can include: "html", "md", "mermaid"
        Default: all three.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        stem = Path(doc.path).stem
        formats = formats or ["html", "md", "mermaid"]
        written: list[Path] = []

        if "html" in formats:
            html = generate_html_report(doc, self._struct, self._code_inv, self._toon)
            p = out / f"{stem}_report.html"
            p.write_text(html, encoding="utf-8")
            written.append(p)
            print(f"[mdflow] ✓ {p}")

        if "md" in formats:
            md = generate_markdown_report(doc, self._struct, self._code_inv, self._toon)
            p = out / f"{stem}_report.md"
            p.write_text(md, encoding="utf-8")
            written.append(p)
            print(f"[mdflow] ✓ {p}")

        if "mermaid" in formats:
            written += self._write_mermaid_files(doc, out, stem)

        return written

    def scan(
        self,
        root: str | Path,
        output_dir: str | Path = ".",
        formats: list[str] | None = None,
    ):
        """
        Parse all .md files in a directory, generate reports, and build a
        cross-document dependency graph report.
        """
        docs = self.parse_dir(root)
        print(f"[mdflow] Parsed {len(docs)} documents")

        out = Path(output_dir)
        for doc in docs:
            self.report(doc, out / "per_file", formats)

        # Cross-document dependency graph
        graph = self.dependency_graph(docs)
        dep_diag = mm.dependency_diagram(graph)
        if dep_diag:
            p = out / "dependency_graph.mermaid"
            p.write_text(dep_diag, encoding="utf-8")
            print(f"[mdflow] ✓ {p}")

            # HTML wrapper for the dependency graph
            self._write_dep_graph_html(graph, dep_diag, out)

        return docs, graph

    # ── diagrams only ─────────────────────────────────────────────────────────

    def diagrams(self, doc: MdDocument) -> dict[str, str]:
        """
        Return all diagrams as strings (keyed by name) without writing files.
        Useful for embedding in other tools.
        """
        tree = self._struct.heading_tree(doc)
        sections = self._struct.section_summary(doc)
        inventory = self._code_inv.inventory(doc)
        metrics = self._toon.metrics(doc)

        return {
            "heading_mindmap": mm.heading_tree_diagram(tree, doc.title),
            "section_flow": mm.section_flowchart(sections),
            "code_pie": mm.code_inventory_pie(inventory),
            "markpact_graph": mm.markpact_graph(inventory, doc.title),
            "alerts_graph": mm.alerts_diagram(metrics),
            "workflow": mm.workflow_diagram(doc),
        }

    # ── internal helpers ──────────────────────────────────────────────────────

    def _write_mermaid_files(self, doc: MdDocument, out: Path, stem: str) -> list[Path]:
        diagrams = self.diagrams(doc)
        written: list[Path] = []
        for name, diagram in diagrams.items():
            if diagram:
                p = out / f"{stem}_{name}.mermaid"
                p.write_text(diagram, encoding="utf-8")
                written.append(p)
                print(f"[mdflow] ✓ {p}")
        return written

    def _write_dep_graph_html(self, graph: DependencyGraph, diagram: str, out: Path):
        from .generators.html import _MERMAID_JS, _CSS

        escaped = diagram.replace("<", "&lt;").replace(">", "&gt;")
        html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>mdflow · Dependency Graph</title>{_CSS}{_MERMAID_JS}</head>
<body><div class="container">
<header><h1>Document Dependency Graph</h1>
<div class="subtitle">{len(graph.nodes)} nodes · {len(graph.edges)} edges</div></header>
<div class="section"><div class="mermaid-wrap">
<pre class="mermaid">{escaped}</pre></div></div>
<footer>generated by mdflow</footer>
</div></body></html>"""
        p = out / "dependency_graph.html"
        p.write_text(html, encoding="utf-8")
        print(f"[mdflow] ✓ {p}")

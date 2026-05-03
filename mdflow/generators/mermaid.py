"""
mdflow.generators.mermaid — generate Mermaid diagrams from analysis results.
"""

from __future__ import annotations
import re
from pathlib import Path
from ..models import MdDocument, DependencyGraph


def _safe_id(s: str) -> str:
    """Mermaid-safe node id."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", s)[:40]


def _short_label(s: str, max_len: int = 30) -> str:
    # Strip characters that break Mermaid node labels: backticks, parens, brackets
    s = re.sub(r'[`()\[\]{}"#]', "", s)
    s = s.strip()
    if len(s) > max_len:
        return s[: max_len - 3] + "..."
    return s


# ─── heading structure ────────────────────────────────────────────────────────


def heading_tree_diagram(tree: list[dict], title: str = "Document Structure") -> str:
    """Mermaid mindmap of heading hierarchy."""
    safe_title = _short_label(title, 40)
    lines = ["mindmap", f"  root(({safe_title}))"]

    def _render(nodes: list[dict], depth: int = 2):
        indent = "  " * depth
        for node in nodes:
            label = _short_label(node["text"])
            lines.append(f"{indent}{label}")
            if node["children"]:
                _render(node["children"], depth + 1)

    _render(tree)
    return "\n".join(lines)


def section_flowchart(sections: list[dict], title: str = "") -> str:
    """Mermaid flowchart showing sections with their code/link counts."""
    lines = ["flowchart TD"]
    if title:
        lines.append(f'  TITLE["{title}"]')

    prev_id = "TITLE" if title else None

    for i, sec in enumerate(sections):
        nid = f"S{i}_{_safe_id(sec['anchor'])}"
        label = _short_label(sec["heading"])
        annotations = []
        if sec["code_blocks"]:
            langs = ", ".join(sec["languages"])
            annotations.append(f"📦 {sec['code_blocks']} code blocks [{langs}]")
        if sec["markpact"]:
            annotations.append(f"🏷 markpact: {', '.join(sec['markpact'])}")
        if sec["links"]:
            annotations.append(f"🔗 {sec['links']} links")

        if annotations:
            ann_str = "\\n".join(annotations)
            lines.append(f'  {nid}["{label}\\n{ann_str}"]')
        else:
            lines.append(f'  {nid}["{label}"]')

        if prev_id:
            lines.append(f"  {prev_id} --> {nid}")
        prev_id = nid

    return "\n".join(lines)


# ─── dependency graph ─────────────────────────────────────────────────────────


def dependency_diagram(graph: DependencyGraph) -> str:
    """Mermaid flowchart of cross-document dependencies."""
    lines = ["flowchart LR"]

    for node in graph.nodes:
        nid = _safe_id(node)
        label = Path(node).name if node.endswith(".md") else _short_label(node, 35)
        lines.append(f'  {nid}["{label}"]')

    edge_kinds = {
        "link": "-->",
        "embed": "-. embed .->",
        "import": "==>",
        "references": "-->",
    }
    for edge in graph.edges:
        src = _safe_id(edge.source)
        tgt = _safe_id(edge.target)
        arrow = edge_kinds.get(edge.kind, "-->")
        label = _short_label(edge.label, 20) if edge.label else ""
        if label:
            lines.append(f'  {src} {arrow}|"{label}"| {tgt}')
        else:
            lines.append(f"  {src} {arrow} {tgt}")

    return "\n".join(lines)


# ─── code block inventory ─────────────────────────────────────────────────────


def code_inventory_pie(inventory: dict) -> str:
    """Mermaid pie chart of code blocks by language."""
    if not inventory["by_language"]:
        return ""
    lines = ["pie title Code Blocks by Language"]
    for lang, items in inventory["by_language"].items():
        label = lang if lang else "unknown"
        lines.append(f'  "{label}" : {len(items)}')
    return "\n".join(lines)


def markpact_graph(inventory: dict, doc_title: str = "Document") -> str:
    """Mermaid graph of markpact embedded file references."""
    if not inventory["by_markpact"]:
        return ""

    lines = ["flowchart TD"]
    doc_id = _safe_id(doc_title)
    lines.append(f'  {doc_id}["{_short_label(doc_title)}"]')
    lines.append(f"  style {doc_id} fill:#2563eb,color:#fff")

    for mp_type, items in inventory["by_markpact"].items():
        for i, item in enumerate(items):
            nid = f"MP_{_safe_id(mp_type)}_{i}"
            path = item.get("path") or f"{mp_type}_{i}"
            label = f"{mp_type}\\n{_short_label(path, 25)}"
            lines.append(f'  {nid}["{label}"]')
            lines.append(f"  {doc_id} -. markpact .-> {nid}")

    return "\n".join(lines)


# ─── TOON alerts / refactors ──────────────────────────────────────────────────


def alerts_diagram(metrics: dict) -> str:
    """Mermaid flowchart of TOON alerts and refactor recommendations."""
    alerts = metrics.get("alerts", [])
    refactors = metrics.get("refactors", [])

    if not alerts and not refactors:
        return ""

    lines = ["flowchart TD"]
    lines.append('  ROOT["🔍 Code Quality Issues"]')
    lines.append("  style ROOT fill:#dc2626,color:#fff")

    if alerts:
        lines.append('  ALERTS["⚠ Alerts"]')
        lines.append("  ROOT --> ALERTS")
        for i, a in enumerate(alerts[:10]):
            nid = f"A{i}"
            label = _short_label(a, 35)
            lines.append(f'  {nid}["{label}"]')
            lines.append(f"  ALERTS --> {nid}")
            lines.append(f"  style {nid} fill:#fef3c7")

    if refactors:
        lines.append('  REFACTORS["🔧 Refactor Tasks"]')
        lines.append("  ROOT --> REFACTORS")
        for i, r in enumerate(refactors[:10]):
            nid = f"R{i}"
            label = _short_label(r, 35)
            lines.append(f'  {nid}["{label}"]')
            lines.append(f"  REFACTORS --> {nid}")
            lines.append(f"  style {nid} fill:#d1fae5")

    return "\n".join(lines)


def workflow_diagram(doc: MdDocument) -> str:
    """Extract workflow steps from DOQL/CSS code blocks and render as flowchart."""
    wf_blocks = [cb for cb in doc.code_blocks if cb.markpact_type == "doql"]
    if not wf_blocks:
        return ""

    lines = ["flowchart TD"]
    wf_re = re.compile(r'workflow\[name="([^"]+)"\]')

    for cb in wf_blocks[:1]:  # first doql block
        workflows = wf_re.findall(cb.content)
        prev_wf = None
        for wf in workflows[:12]:
            wid = _safe_id(wf)
            lines.append(f'  {wid}["{wf}"]')
            if prev_wf:
                lines.append(f"  {_safe_id(prev_wf)} --> {wid}")
            prev_wf = wf

    return "\n".join(lines) if len(lines) > 1 else ""

"""
mdflow.generators.html — generate a self-contained HTML analysis report.
"""
from __future__ import annotations
from ..models import MdDocument
from . import mermaid as mm


_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;700&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0f1117; --panel: #1a1d27; --border: #2a2d3a;
    --accent: #3b82f6; --accent2: #8b5cf6; --ok: #10b981;
    --warn: #f59e0b; --err: #ef4444;
    --text: #e2e8f0; --muted: #64748b;
    --mono: 'IBM Plex Mono', monospace;
    --sans: 'IBM Plex Sans', sans-serif;
  }
  body { background: var(--bg); color: var(--text); font-family: var(--sans); font-size: 14px; line-height: 1.6; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
  header { border-bottom: 2px solid var(--accent); padding-bottom: 1.5rem; margin-bottom: 2rem; }
  header h1 { font-size: 2rem; font-weight: 700; color: #fff; }
  header .subtitle { color: var(--muted); font-family: var(--mono); font-size: 0.85rem; margin-top: 0.25rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 2rem; }
  .card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; }
  .card h3 { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 0.75rem; }
  .card .value { font-size: 2rem; font-weight: 700; font-family: var(--mono); color: var(--accent); }
  .card .label { font-size: 0.8rem; color: var(--muted); margin-top: 0.2rem; }
  .section { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
  .section h2 { font-size: 1rem; font-weight: 600; border-bottom: 1px solid var(--border); padding-bottom: 0.75rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
  .section h2 .icon { font-size: 1.1rem; }
  .mermaid-wrap { background: #fff; border-radius: 6px; padding: 1rem; overflow-x: auto; margin-top: 0.5rem; }
  pre.code-raw { background: #0a0c14; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; overflow-x: auto; font-family: var(--mono); font-size: 0.8rem; color: #94a3b8; white-space: pre; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: 0.5rem 0.75rem; background: #12151f; color: var(--muted); font-weight: 500; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); }
  td { padding: 0.5rem 0.75rem; border-bottom: 1px solid #1e2133; }
  tr:last-child td { border-bottom: none; }
  .badge { display: inline-block; padding: 0.2em 0.6em; border-radius: 4px; font-size: 0.7rem; font-family: var(--mono); font-weight: 600; }
  .badge-lang { background: #1e3a5f; color: #93c5fd; }
  .badge-mp { background: #3b1f5e; color: #c4b5fd; }
  .badge-warn { background: #451a03; color: #fcd34d; }
  .tag-list { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
  .pill { display: inline-block; padding: 0.15em 0.6em; border-radius: 20px; font-size: 0.72rem; font-family: var(--mono); background: #1e2133; color: var(--muted); border: 1px solid var(--border); }
  .pill.active { background: #1e3a5f; color: var(--accent); border-color: var(--accent); }
  .alert-list { list-style: none; }
  .alert-list li { padding: 0.4rem 0.75rem; border-left: 3px solid var(--warn); margin-bottom: 0.4rem; background: #1c1a12; font-family: var(--mono); font-size: 0.8rem; border-radius: 0 4px 4px 0; }
  .refactor-list li { border-left-color: var(--ok); background: #0d1f18; }
  .meta-table td:first-child { color: var(--muted); font-family: var(--mono); width: 35%; }
  footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.75rem; text-align: center; font-family: var(--mono); }
</style>
"""

_MERMAID_JS = """
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });
</script>
"""


def _card(title: str, value: str, label: str = "") -> str:
    return f"""<div class="card">
  <h3>{title}</h3>
  <div class="value">{value}</div>
  {"<div class='label'>" + label + "</div>" if label else ""}
</div>"""


def _mermaid_block(diagram: str) -> str:
    if not diagram:
        return ""
    escaped = diagram.replace("<", "&lt;").replace(">", "&gt;")
    return f'<div class="mermaid-wrap"><pre class="mermaid">{escaped}</pre></div>'


def generate_html_report(
    doc: MdDocument,
    structure_analyzer,
    code_analyzer,
    toon_analyzer,
) -> str:
    """Generate a full self-contained HTML report for a document."""

    heading_tree = structure_analyzer.heading_tree(doc)
    sections = structure_analyzer.section_summary(doc)
    inventory = code_analyzer.inventory(doc)
    metrics = toon_analyzer.metrics(doc)

    # ── summary cards ─────────────────────────────────────────────────────────
    cards_html = '<div class="grid">'
    cards_html += _card("Headings", str(len(doc.headings)), "sections & subsections")
    cards_html += _card("Code Blocks", str(inventory["total"]),
                        f"{len(inventory['by_language'])} languages")
    cards_html += _card("Links", str(len(doc.links)),
                        f"{len(doc.internal_links)} internal · {len(doc.external_links)} external")
    cards_html += _card("Markpact refs", str(len(inventory["markpact_paths"])),
                        "embedded file references")
    if metrics["health"].get("cc_mean"):
        cards_html += _card("CC̄", str(metrics["health"]["cc_mean"]), "mean cyclomatic complexity")
    if metrics["health"].get("critical"):
        cards_html += _card("Critical", str(metrics["health"]["critical"]), "functions above CC limit")
    cards_html += "</div>"

    # ── metadata table ────────────────────────────────────────────────────────
    meta_rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in doc.metadata.items()
    )
    meta_section = ""
    if meta_rows:
        meta_section = f"""<div class="section">
  <h2><span class="icon">🔖</span> Metadata</h2>
  <table class="meta-table"><tbody>{meta_rows}</tbody></table>
</div>"""

    # ── structure diagram ─────────────────────────────────────────────────────
    structure_diag = mm.heading_tree_diagram(heading_tree, doc.title)
    section_flow = mm.section_flowchart(sections, "")

    # ── code inventory ────────────────────────────────────────────────────────
    lang_rows = "".join(
        f"<tr><td><span class='badge badge-lang'>{lang}</span></td>"
        f"<td>{len(items)}</td>"
        f"<td>{sum(i['lines'] for i in items)}</td>"
        f"<td>{'Yes' if any(i['markpact'] for i in items) else '—'}</td></tr>"
        for lang, items in inventory["by_language"].items()
    )
    markpact_rows = "".join(
        f"<tr><td><span class='badge badge-mp'>markpact:{mp_type}</span></td>"
        f"<td>{len(items)}</td>"
        f"<td>{', '.join(i.get('path','—') or '—' for i in items[:3])}</td></tr>"
        for mp_type, items in inventory["by_markpact"].items()
    )

    pie_diag = mm.code_inventory_pie(inventory) if inventory["total"] else ""
    mp_diag = mm.markpact_graph(inventory, doc.title)

    # ── TOON alerts ───────────────────────────────────────────────────────────
    alert_items = "".join(f"<li>{a}</li>" for a in metrics.get("alerts", []))
    refactor_items = "".join(f"<li>{r}</li>" for r in metrics.get("refactors", []))
    toon_diag = mm.alerts_diagram(metrics)

    # ── workflow diagram ──────────────────────────────────────────────────────
    wf_diag = mm.workflow_diagram(doc)

    # ── links table ───────────────────────────────────────────────────────────
    link_rows = "".join(
        f"<tr><td>{l.line}</td><td><code>{l.href[:60]}</code></td>"
        f"<td><span class='badge badge-lang'>{l.kind}</span></td>"
        f"<td>{l.text[:40]}</td></tr>"
        for l in doc.links[:50]
    )

    # ── TOON sections list ────────────────────────────────────────────────────
    toon_pills = "".join(
        f"<span class='pill active'>{ts.name}</span>"
        for ts in doc.toon_sections
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>mdflow · {doc.title}</title>
  {_CSS}
  {_MERMAID_JS}
</head>
<body>
<div class="container">

<header>
  <h1>{doc.title}</h1>
  <div class="subtitle">mdflow analysis · {doc.path}</div>
</header>

{cards_html}

{meta_section}

{"<div class='section'><h2><span class='icon'>🏷</span> TOON Sections Detected</h2><div class='tag-list'>" + toon_pills + "</div></div>" if toon_pills else ""}

<div class="section">
  <h2><span class="icon">🗂</span> Document Structure</h2>
  {_mermaid_block(structure_diag)}
</div>

<div class="section">
  <h2><span class="icon">📋</span> Section Flow with Annotations</h2>
  {_mermaid_block(section_flow)}
</div>

{"<div class='section'><h2><span class='icon'>📦</span> Code Block Inventory</h2>" + 
  "<table><thead><tr><th>Language</th><th>Blocks</th><th>Lines</th><th>Markpact</th></tr></thead><tbody>" +
  lang_rows + "</tbody></table>" +
  (_mermaid_block(pie_diag) if pie_diag else "") +
  ("</div>" if lang_rows else "") if lang_rows else ""}

{"<div class='section'><h2><span class='icon'>🏷</span> Markpact Embedded Files</h2>" +
  "<table><thead><tr><th>Type</th><th>Count</th><th>Paths</th></tr></thead><tbody>" +
  markpact_rows + "</tbody></table>" +
  _mermaid_block(mp_diag) +
  "</div>" if markpact_rows else ""}

{"<div class='section'><h2><span class='icon'>⚡</span> Workflows (DOQL)</h2>" + _mermaid_block(wf_diag) + "</div>" if wf_diag else ""}

{"<div class='section'><h2><span class='icon'>⚠</span> Quality Alerts &amp; Refactor Tasks</h2>" +
  ("<ul class='alert-list'>" + alert_items + "</ul>" if alert_items else "") +
  ("<ul class='alert-list refactor-list'>" + refactor_items + "</ul>" if refactor_items else "") +
  _mermaid_block(toon_diag) + "</div>" if (alert_items or refactor_items) else ""}

{"<div class='section'><h2><span class='icon'>🔗</span> Links</h2>" +
  "<table><thead><tr><th>Line</th><th>URL</th><th>Kind</th><th>Text</th></tr></thead><tbody>" +
  link_rows + "</tbody></table></div>" if link_rows else ""}

<footer>generated by mdflow · markdown dependency analyzer</footer>

</div>
</body>
</html>"""

    return html

# mdflow


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.3-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.30-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-2.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.3000 (2 commits)
- 👤 **Human dev:** ~$200 (2.0h @ $100/h, 30min dedup)

Generated on 2026-05-03 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

**Markdown dependency analyzer — extract all dependencies, generate diagrams and charts.**

`mdflow` parses Markdown files and extracts every possible structural element:
headings, links, fenced code blocks (including `markpact:*` embedded file references),
list items, TOON/YAML quality sections, and document metadata.
It then generates Mermaid diagrams, HTML reports, and Markdown summaries.

---

## What it extracts

| Element | Details |
|---|---|
| **Headings** | Full H1–H6 hierarchy, anchor slugs |
| **Links** | `[text](href)` — classified as internal / external / anchor / image |
| **Code blocks** | Language, content, line range, `markpact:type path=...` metadata |
| **List items** | Depth, parent heading, clean text |
| **TOON sections** | ALERTS, REFACTOR, HOTSPOTS, HEALTH, NEXT, RISKS, PIPELINES… |
| **Document metadata** | `## Metadata` key/value lists |
| **Cross-doc dependencies** | Links between files, `markpact` embedded file paths |

---

## Generated outputs

| Output | Description |
|---|---|
| `{stem}_report.html` | Self-contained HTML report with all diagrams (Mermaid.js) |
| `{stem}_report.md` | Markdown summary with inline Mermaid |
| `{stem}_heading_mindmap.mermaid` | Mindmap of heading hierarchy |
| `{stem}_section_flow.mermaid` | Section flowchart with code/link annotations |
| `{stem}_code_pie.mermaid` | Pie chart of code blocks by language |
| `{stem}_markpact_graph.mermaid` | Graph of embedded file references |
| `{stem}_alerts_graph.mermaid` | TOON alerts & refactor tasks flowchart |
| `{stem}_workflow.mermaid` | DOQL workflow steps diagram |
| `dependency_graph.html` | Cross-document dependency graph (directory scan) |

---

## Installation

```bash
# Clone or copy the mdflow/ directory, then:
pip install -e .
# No mandatory dependencies — pure stdlib.
```

---

## Usage

### Python API

```python
from mdflow import MdFlow

flow = MdFlow()

# ── Single file ───────────────────────────────────────────────
doc = flow.parse("SUMR.md")

print(doc.title)                        # "Ze źródeł"
print(len(doc.headings))               # 24
print([ts.name for ts in doc.toon_sections])  # ['HEALTH', 'REFACTOR', ...]
print(doc.metadata)                    # {'name': 'redsl', 'version': '1.2.45', ...}

# Access markpact embedded file references
for cb in doc.markpact_blocks:
    print(f"markpact:{cb.markpact_type}  path={cb.markpact_path}")

# Get TOON quality metrics
metrics = flow.toon_metrics(doc)
print(metrics["health"])               # {'cc_mean': 20.0, 'critical': 7}
print(metrics["refactors"][:3])        # list of refactor tasks

# Get all Mermaid diagrams as strings (no files written)
diagrams = flow.diagrams(doc)
print(diagrams["section_flow"])        # flowchart TD ...

# Generate reports to disk
flow.report(doc, "output/")            # writes HTML + MD + .mermaid files

# ── Directory scan ────────────────────────────────────────────
docs, graph = flow.scan("docs/", "output/")
print(f"{len(docs)} files, {len(graph.edges)} dependency edges")
```

### CLI

```bash
# Analyze a single file
mdflow analyze SUMR.md --output output/

# Select formats
mdflow analyze SUMR.md --format html,md

# Scan a directory
mdflow scan docs/ --output output/

# Print a specific Mermaid diagram to stdout
mdflow diagram SUMR.md --diagram section_flow
mdflow diagram SUMR.md --diagram list        # list available diagrams

# Write diagram to file
mdflow diagram SUMR.md --diagram alerts_graph -o alerts.mermaid
```

## Examples

The `examples/` directory contains comprehensive usage examples:

- **basic_usage.py** - Basic parsing and report generation
- **advanced_analysis.py** - Structure analysis, code inventory, TOON metrics
- **directory_scan.py** - Scanning multiple files and dependency graphs
- **custom_diagrams.py** - Working with diagrams programmatically
- **cli_usage.sh** - CLI usage examples

Run examples from the project root:
```bash
python examples/basic_usage.py
python examples/advanced_analysis.py
python examples/directory_scan.py
python examples/custom_diagrams.py
bash examples/cli_usage.sh
```

See [examples/README.md](examples/README.md) for detailed documentation.

---

## Architecture

```
mdflow/
├── __init__.py         ← MdFlow façade (high-level API)
├── models.py           ← Data classes: MdDocument, DependencyGraph, …
├── parser.py           ← Core Markdown parser (stdlib only)
├── analyzers/
│   └── __init__.py     ← DependencyAnalyzer, StructureAnalyzer,
│                          CodeInventoryAnalyzer, ToonAnalyzer
├── generators/
│   ├── __init__.py
│   ├── mermaid.py      ← All Mermaid diagram generators
│   ├── html.py         ← Self-contained HTML report
│   └── markdown.py     ← Markdown summary report
└── cli.py              ← argparse CLI entry point
```

---

## Supported TOON sections

`mdflow` recognises these TOON section names inside `toon` / `yaml` code blocks
and in blocks tagged `markpact:analysis`:

`ALERTS` · `REFACTOR` · `HOTSPOTS` · `HEALTH` · `NEXT` · `RISKS` · `PIPELINES`
· `DUPLICATES` · `WARNINGS` · `MODULES` · `EVOLUTION` · `COUPLING`

---

## Extension points

- **Custom extractor**: subclass or monkey-patch `MdParser`
- **Custom diagram**: call `flow.diagrams(doc)` and extend the `mermaid` module
- **Graphviz output**: install `graphviz` Python package and use
  `DependencyGraph` data directly

---

## License

Licensed under Apache-2.0.

# mdflow

## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.7-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$1.02-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-6.2h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $1.0235 (8 commits)
- 👤 **Human dev:** ~$624 (6.2h @ $100/h, 30min dedup)

Generated on 2026-07-06 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

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

## Mermaid validation

Every generated `.mermaid` file is automatically validated before writing.
Detected issues are printed inline and written as tickets to `TODO.md`:

```
[mdflow] ⚠ 1 error(s) output/SUMR_section_flow.mermaid
  ✗ [BACKTICK_IN_LABEL] Backtick inside node label (line 5): ...
[mdflow] → 1 validation ticket(s) written to TODO.md
```

Validation checks: `EMPTY_DIAGRAM`, `NO_DIAGRAM_TYPE`, `BACKTICK_IN_LABEL`,
`DUPLICATE_NODE_ID`, `MINDMAP_ILLEGAL_CHARS`.

---

## Quality tooling

mdflow uses [`prefact`](https://github.com/semcod/prefact) and
[`pyqual`](https://github.com/semcod/pyqual) for automated code quality gates.

```bash
# Run full quality loop (prefact scan → ruff → pytest → LLM fix on fail)
task quality          # alias: pyqual run

# Scan for code issues (duplicate imports, wildcard imports, …)
task prefact          # alias: prefact scan -p .

# Auto-fix detected issues
task prefact-fix      # alias: prefact fix -p .
```

A **git pre-commit hook** (`.git/hooks/pre-commit`) runs all checks automatically
before every commit and blocks on failures, writing tickets to `TODO.md`.

---

## Testing

### Unit tests

```bash
pytest tests/ -v
```

### E2E / CLI tests (TestQL)

142 scenarios covering CLI commands, output file validation, and integration
with real semcod workspace projects:

```bash
# All scenarios
task testql-run

# Smoke only (help, subcommands)
task testql-smoke

# Full E2E (analyze, scan, diagram, semcod projects, mermaid validation)
task testql-e2e

# Single scenario
testql run testql-scenarios/02_cli_analyze_e2e.testql.toon.yaml
```

Scenarios in `testql-scenarios/`:

| File | Tests | Scope |
|---|---|---|
| `01_cli_help_version` | 16 | help, subcommand help |
| `02_cli_analyze_e2e` | 35 | analyze: HTML/MD/mermaid output |
| `03_cli_scan_e2e` | 13 | scan: per_file output, dependency graph |
| `04_cli_diagram_e2e` | 23 | diagram: list, stdout, file, unknown name |
| `05_e2e_semcod_projects` | 30 | prefact, pyqual, planfile, goal SUMD.md |
| `06_e2e_mermaid_validation` | 22 | backtick-free labels, pie title format |

---

## Architecture

```
mdflow/
├── __init__.py         ← MdFlow façade (high-level API)
├── models.py           ← Data classes: MdDocument, DependencyGraph, …
├── parser.py           ← Core Markdown parser (stdlib only)
├── validators.py       ← Mermaid diagram validator + TODO.md ticket writer
├── analyzers/
│   └── __init__.py     ← DependencyAnalyzer, StructureAnalyzer,
│                          CodeInventoryAnalyzer, ToonAnalyzer
├── generators/
│   ├── __init__.py
│   ├── mermaid.py      ← All Mermaid diagram generators
│   ├── html.py         ← Self-contained HTML report (split into helpers)
│   └── markdown.py     ← Markdown summary report (split into helpers)
└── cli.py              ← argparse CLI entry point
```

---

## Examples

### Basic

- **`examples/basic/01_parse_single_file.py`** — Parse and inspect a single document
- **`examples/basic/02_generate_reports.py`** — Generate HTML, Markdown, and Mermaid reports
- **`examples/basic/03_diagrams_as_strings.py`** — Get diagrams as strings (no file I/O)
- **`examples/basic/04_cli_basics.sh`** — CLI: `analyze`, `scan`, `diagram`

### Advanced

- **`examples/advanced/01_directory_scan.py`** — Scan a directory, build dependency graphs
- **`examples/advanced/02_toon_analysis.py`** — Extract TOON quality metrics
- **`examples/advanced/03_custom_diagram_pipeline.py`** — Custom HTML with selected diagrams

### API / Extensibility

- **`examples/api/01_low_level_parser.py`** — Use `MdParser` directly
- **`examples/api/02_custom_analyzer.py`** — Build your own analyzer

### semcod workspace

- **`examples/semcod/analyze_prefact.py`** — Parse `prefact/SUMD.md`, extract TOON metrics
- **`examples/semcod/scan_semcod_workspace.py`** — Scan 6 semcod projects, cross-project TOON summary
- **`examples/semcod/toon_comparison.py`** — CC/alerts/refactors comparison table across projects
- **`examples/semcod/04_cli_semcod.sh`** — CLI shell examples for the semcod workspace

```bash
python examples/semcod/toon_comparison.py
python examples/semcod/scan_semcod_workspace.py
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

## Dependency maintenance

See [dependency updates and Python tool groups](docs/dependencies.md) for locked tests, daily updates and freshness checks.

<!-- code2docs:start --># mdflow

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.11-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-177-green)
> **177** functions | **25** classes | **34** files | CC̄ = 5.4

> Auto-generated project documentation from source code analysis.

**Author:** Tom Softreck <tom@sapletta.com>  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/semcod/mdflow](https://github.com/semcod/mdflow)

## Installation

### From PyPI

```bash
pip install mdflow
```

### From Source

```bash
git clone https://github.com/semcod/mdflow
cd mdflow
pip install -e .
```

### Optional Extras

```bash
pip install mdflow[graphviz]    # graphviz features
pip install mdflow[dev]    # development tools
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
mdflow ./my-project

# Only regenerate README
mdflow ./my-project --readme-only

# Preview what would be generated (no file writes)
mdflow ./my-project --dry-run

# Check documentation health
mdflow check ./my-project

# Sync — regenerate only changed modules
mdflow sync ./my-project
```

### Python API

```python
from mdflow import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```




## Architecture

```
mdflow/
├── SUMR
├── fix
├── goal
├── pyproject
├── tree
├── TODO
├── CHANGELOG
├── project
├── example
├── README
    ├── custom_diagrams
    ├── directory_scan
    ├── advanced_analysis
    ├── cli_usage
    ├── README
    ├── basic_usage
    ├── cli
├── mdflow/
    ├── parser
    ├── models
        ├── markdown
    ├── generators/
        ├── html
        ├── mermaid
    ├── analyzers/
    ├── prompt
        ├── toon
    ├── README
        ├── toon
        ├── toon
        ├── toon
        ├── toon
    ├── context
    ├── calls
```

## API Overview

### Classes

- **`HistoryEvent`** — —
- **`HistoryWriter`** — —
- **`HistoryReader`** — —
- **`ConsciousnessLoop`** — —
- **`LLMConfig`** — —
- **`MemoryConfig`** — —
- **`AnalyzerConfig`** — —
- **`RefactorConfig`** — —
- **`AgentConfig`** — —
- **`CycleReport`** — —
- **`RefactorOrchestrator`** — —
- **`MdFlow`** — High-level façade for the mdflow library.
- **`MdParser`** — Parse a single Markdown file into an MdDocument.
- **`Heading`** — —
- **`Link`** — —
- **`CodeBlock`** — —
- **`ListItem`** — —
- **`ToonSection`** — A named TOON/YAML embedded block (from code blocks with toon language).
- **`MdDocument`** — Full parsed representation of one Markdown file.
- **`DependencyEdge`** — —
- **`DependencyGraph`** — —
- **`DependencyAnalyzer`** — Build a cross-document dependency graph from a list of MdDocuments.
- **`StructureAnalyzer`** — Analyse the heading/section structure of a single document.
- **`CodeInventoryAnalyzer`** — Inventory all code blocks by language, markpact type, and path.
- **`ToonAnalyzer`** — Extract structured metrics from embedded TOON sections.

### Functions

- `cmd_analyze()` — —
- `cmd_explain()` — —
- `cmd_refactor()` — —
- `cmd_memory_stats()` — —
- `cmd_serve()` — —
- `main()` — —
- `record()` — —
- `record_event()` — —
- `decision_signature()` — —
- `has_recent_signature()` — —
- `load_events()` — —
- `filter_by_file()` — —
- `filter_by_type()` — —
- `has_recent_proposal()` — —
- `has_recent_ticket()` — —
- `generate_decision_report()` — —
- `main_loop()` — —
- `run()` — —
- `stop()` — —
- `is_local()` — —
- `api_key()` — —
- `from_env()` — —
- `run_cycle()` — —
- `run_from_toon_content()` — —
- `add_custom_rules()` — —
- `print()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `cmd_analyze(args)` — —
- `cmd_scan(args)` — —
- `cmd_diagram(args)` — —
- `main()` — —
- `generate_markdown_report(doc, structure_analyzer, code_analyzer, toon_analyzer)` — —
- `generate_html_report(doc, structure_analyzer, code_analyzer, toon_analyzer)` — Generate a full self-contained HTML report for a document.
- `heading_tree_diagram(tree, title)` — Mermaid mindmap of heading hierarchy.
- `section_flowchart(sections, title)` — Mermaid flowchart showing sections with their code/link counts.
- `dependency_diagram(graph)` — Mermaid flowchart of cross-document dependencies.
- `code_inventory_pie(inventory)` — Mermaid pie chart of code blocks by language.
- `markpact_graph(inventory, doc_title)` — Mermaid graph of markpact embedded file references.
- `alerts_diagram(metrics)` — Mermaid flowchart of TOON alerts and refactor recommendations.
- `workflow_diagram(doc)` — Extract workflow steps from DOQL/CSS code blocks and render as flowchart.
- `generate_html_report()` — —
- `generate_markdown_report()` — —
- `main()` — —
- `heading_tree_diagram()` — —
- `section_flowchart()` — —
- `dependency_diagram()` — —
- `code_inventory_pie()` — —
- `markpact_graph()` — —
- `alerts_diagram()` — —
- `workflow_diagram()` — —
- `cmd_analyze()` — —
- `cmd_scan()` — —
- `cmd_diagram()` — —
- `print()` — —
- `cmd_explain()` — —
- `cmd_refactor()` — —
- `cmd_memory_stats()` — —
- `cmd_serve()` — —
- `record()` — —
- `record_event()` — —
- `decision_signature()` — —
- `has_recent_signature()` — —
- `load_events()` — —
- `filter_by_file()` — —
- `filter_by_type()` — —
- `has_recent_proposal()` — —
- `has_recent_ticket()` — —
- `generate_decision_report()` — —
- `main_loop()` — —
- `run()` — —
- `stop()` — —
- `is_local()` — —
- `api_key()` — —
- `from_env()` — —
- `run_cycle()` — —
- `run_from_toon_content()` — —
- `add_custom_rules()` — —


## Project Structure

📄 `CHANGELOG`
📄 `README` (1 functions)
📄 `SUMR` (57 functions, 11 classes)
📄 `TODO`
📄 `example`
📄 `examples.README`
📄 `examples.advanced_analysis` (1 functions)
📄 `examples.basic_usage` (1 functions)
📄 `examples.cli_usage`
📄 `examples.custom_diagrams` (1 functions)
📄 `examples.directory_scan` (1 functions)
📄 `fix`
📄 `goal`
📦 `mdflow` (12 functions, 1 classes)
📦 `mdflow.analyzers` (7 functions, 4 classes)
📄 `mdflow.cli` (4 functions)
📦 `mdflow.generators`
📄 `mdflow.generators.html` (3 functions)
📄 `mdflow.generators.markdown` (1 functions)
📄 `mdflow.generators.mermaid` (9 functions)
📄 `mdflow.models` (2 functions, 8 classes)
📄 `mdflow.parser` (7 functions, 1 classes)
📄 `project`
📄 `project.README`
📄 `project.analysis.toon`
📄 `project.calls`
📄 `project.calls.toon`
📄 `project.context`
📄 `project.evolution.toon`
📄 `project.map.toon` (84 functions)
📄 `project.project.toon`
📄 `project.prompt`
📄 `pyproject`
📄 `tree`

## Requirements

- Python >= >=3.11
- goal >=2.1.0- costs >=0.1.20- pfix >=0.1.60

## Contributing

**Contributors:**
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>
- Tom Softreck <tom@sapletta.com>

We welcome contributions! Open an issue or pull request to get started.
### Development Setup

```bash
# Clone the repository
git clone https://github.com/semcod/mdflow
cd mdflow

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `examples` | Usage examples and code samples | [View](./examples) |

<!-- code2docs:end -->
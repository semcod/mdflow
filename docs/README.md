<!-- code2docs:start --># mdflow

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.11-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-145-green)
> **145** functions | **32** classes | **52** files | CC̄ = 5.5

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
├── planfile
├── testql
├── SUMD
├── pyproject
├── tree
├── TODO
├── CHANGELOG
├── Taskfile
├── project
├── example
├── README
    ├── README
    ├── custom_diagrams
    ├── directory_scan
    ├── advanced_analysis
    ├── cli_usage
    ├── README
    ├── basic_usage
        ├── 01_directory_scan
        ├── 03_custom_diagram_pipeline
        ├── 02_toon_analysis
        ├── 02_generate_reports
        ├── 04_cli_basics
        ├── 01_parse_single_file
        ├── 03_diagrams_as_strings
        ├── project_overview
        ├── deployment
        ├── api_reference
    ├── cli
├── mdflow/
    ├── parser
    ├── models
        ├── markdown
    ├── generators/
        ├── html
        ├── mermaid
    ├── analyzers/
        ├── toon
    ├── prompt
            ├── toon
        ├── toon
        ├── toon
        ├── toon
    ├── calls
    ├── context
        ├── toon
    ├── README
        ├── toon
        ├── 01_low_level_parser
```

## API Overview

### Classes

- **`MdParser`** — —
- **`Heading`** — —
- **`Link`** — —
- **`CodeBlock`** — —
- **`ListItem`** — —
- **`ToonSection`** — —
- **`MdDocument`** — —
- **`DependencyEdge`** — —
- **`DependencyGraph`** — —
- **`MdParser`** — —
- **`Heading`** — —
- **`Link`** — —
- **`CodeBlock`** — —
- **`ListItem`** — —
- **`ToonSection`** — —
- **`MdDocument`** — —
- **`DependencyEdge`** — —
- **`DependencyGraph`** — —
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

- `parse()` — —
- `parse_text()` — —
- `internal_links()` — —
- `anchor_links()` — —
- `external_links()` — —
- `markpact_blocks()` — —
- `add_node()` — —
- `add_edge()` — —
- `cmd_analyze()` — —
- `cmd_scan()` — —
- `cmd_diagram()` — —
- `main()` — —
- `main()` — —
- `cmd_analyze()` — —
- `cmd_scan()` — —
- `cmd_diagram()` — —
- `generate_html_report()` — —
- `generate_markdown_report()` — —
- `heading_tree_diagram()` — —
- `section_flowchart()` — —
- `dependency_diagram()` — —
- `code_inventory_pie()` — —
- `markpact_graph()` — —
- `alerts_diagram()` — —
- `workflow_diagram()` — —
- `test_placeholder()` — —
- `test_import()` — —
- `parse()` — —
- `parse_text()` — —
- `internal_links()` — —
- `anchor_links()` — —
- `external_links()` — —
- `markpact_blocks()` — —
- `add_node()` — —
- `add_edge()` — —
- `print()` — —
- `generate_readme()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `process_data()` — —
- `verify_token()` — —
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
- `process_data()` — —
- `verify_token()` — —
- `print()` — —
- `generate_readme()` — —
- `test_placeholder()` — —
- `test_import()` — —
- `parse()` — —
- `parse_text()` — —
- `internal_links()` — —
- `anchor_links()` — —
- `external_links()` — —
- `markpact_blocks()` — —
- `add_node()` — —
- `add_edge()` — —
- `main()` — —


## Project Structure

📄 `CHANGELOG`
📄 `README` (1 functions)
📄 `SUMD` (50 functions, 9 classes)
📄 `SUMR` (17 functions, 9 classes)
📄 `TODO`
📄 `Taskfile`
📄 `docs.README` (1 functions)
📄 `example`
📄 `examples.README`
📄 `examples.advanced.01_directory_scan` (1 functions)
📄 `examples.advanced.02_toon_analysis` (1 functions)
📄 `examples.advanced.03_custom_diagram_pipeline` (1 functions)
📄 `examples.advanced_analysis` (1 functions)
📄 `examples.api.01_low_level_parser` (1 functions)
📄 `examples.basic.01_parse_single_file` (1 functions)
📄 `examples.basic.02_generate_reports` (1 functions)
📄 `examples.basic.03_diagrams_as_strings` (1 functions)
📄 `examples.basic.04_cli_basics`
📄 `examples.basic_usage` (1 functions)
📄 `examples.cli_usage`
📄 `examples.custom_diagrams` (1 functions)
📄 `examples.data.api_reference` (1 functions)
📄 `examples.data.deployment`
📄 `examples.data.project_overview` (1 functions)
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
📄 `planfile`
📄 `project`
📄 `project.README`
📄 `project.analysis.toon`
📄 `project.calls`
📄 `project.calls.toon`
📄 `project.context`
📄 `project.duplication.toon`
📄 `project.evolution.toon`
📄 `project.map.toon` (136 functions)
📄 `project.project.toon`
📄 `project.prompt`
📄 `pyproject`
📄 `testql`
📄 `testql-scenarios.generated-cli-tests.testql.toon`
📄 `tree`

## Requirements

- Python >= >=3.11
- goal >=2.1.0- costs >=0.1.20- pfix >=0.1.60

## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

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
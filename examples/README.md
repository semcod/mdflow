# mdflow Examples

This directory contains usage examples for the mdflow library, organized by complexity and use case.

## Directory Structure

```
examples/
├── data/                          # Sample Markdown files for analysis
│   ├── project_overview.md
│   ├── api_reference.md
│   └── deployment.md
├── basic/                         # Getting started examples
│   ├── 01_parse_single_file.py    # Parse and inspect a single document
│   ├── 02_generate_reports.py     # Generate HTML, MD, Mermaid reports
│   ├── 03_diagrams_as_strings.py  # Get diagrams without writing files
│   └── 04_cli_basics.sh           # CLI usage patterns
├── advanced/                      # Complex workflows
│   ├── 01_directory_scan.py       # Scan directory + dependency graph
│   ├── 02_toon_analysis.py        # Extract TOON quality metrics
│   └── 03_custom_diagram_pipeline.py  # Build custom HTML with diagrams
└── api/                           # Low-level and extensibility
    ├── 01_low_level_parser.py     # Use MdParser directly
    └── 02_custom_analyzer.py      # Build your own analyzer
```

## Prerequisites

Install mdflow from the project root:

```bash
pip install -e .
```

All examples are designed to run from the project root directory.

## Basic Examples

### `01_parse_single_file.py`
Parse a Markdown file and inspect headings, links, code blocks, metadata, and list items.

```bash
python examples/basic/01_parse_single_file.py
```

### `02_generate_reports.py`
Generate HTML, Markdown, and Mermaid reports for a single document.

```bash
python examples/basic/02_generate_reports.py
```

Output goes to `examples/output/basic/`.

### `03_diagrams_as_strings.py`
Get Mermaid diagrams as Python strings without writing files to disk. Useful for embedding in other tools.

```bash
python examples/basic/03_diagrams_as_strings.py
```

### `04_cli_basics.sh`
Demonstrates all CLI commands: `analyze`, `scan`, `diagram`.

```bash
bash examples/basic/04_cli_basics.sh
```

## Advanced Examples

### `01_directory_scan.py`
Scan a directory of Markdown files, build cross-document dependency graphs, and generate per-file reports.

```bash
python examples/advanced/01_directory_scan.py
```

### `02_toon_analysis.py`
Extract and display TOON quality metrics (HEALTH, ALERTS, REFACTOR, RISKS, HOTSPOTS) from structured code blocks.

```bash
python examples/advanced/02_toon_analysis.py
```

### `03_custom_diagram_pipeline.py`
Build a custom HTML page by manually generating selected diagrams and embedding them in your own template.

```bash
python examples/advanced/03_custom_diagram_pipeline.py
```

## API Examples

### `01_low_level_parser.py`
Use `MdParser` directly instead of the `MdFlow` facade for fine-grained control, or parse raw text without a file.

```bash
python examples/api/01_low_level_parser.py
```

### `02_custom_analyzer.py`
Demonstrates how to extend mdflow with custom analysis logic (word frequency, language distribution, dead link detection) using the parsed document model.

```bash
python examples/api/02_custom_analyzer.py
```

## Data Files

The `examples/data/` directory contains three linked Markdown documents that serve as realistic input for all examples:

- `project_overview.md` — Architecture description with mermaid, yaml, and code blocks
- `api_reference.md` — API docs linking back to overview
- `deployment.md` — Deployment guide with TOON health metrics

These files cross-reference each other so directory-scan examples can demonstrate dependency graph generation.

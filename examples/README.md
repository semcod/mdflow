# mdflow Examples

This directory contains usage examples for the mdflow library.

## Python API Examples

### basic_usage.py
Demonstrates basic mdflow usage:
- Parsing a single Markdown file
- Accessing document properties (title, headings, links, code blocks)
- Generating HTML and Markdown reports

Run:
```bash
python examples/basic_usage.py
```

### advanced_analysis.py
Shows advanced analysis capabilities:
- Using built-in analyzers (structure, code inventory, TOON metrics)
- Accessing detailed analysis results
- Working with markpact embedded file references
- Extracting TOON quality metrics (health, alerts, refactors, risks)

Run:
```bash
python examples/advanced_analysis.py
```

### directory_scan.py
Demonstrates directory scanning:
- Scanning an entire directory tree for Markdown files
- Building cross-document dependency graphs
- Generating reports for all files
- Analyzing document summaries

Run:
```bash
python examples/directory_scan.py
```

### custom_diagrams.py
Shows how to work with diagrams:
- Generating diagrams as strings without writing files
- Accessing individual diagram types
- Saving specific diagrams to custom locations
- Embedding diagrams in custom HTML outputs

Run:
```bash
python examples/custom_diagrams.py
```

## CLI Examples

### cli_usage.sh
Bash script demonstrating CLI usage:
- Analyzing single files
- Selecting output formats (html, md, mermaid)
- Scanning directories
- Listing and extracting specific diagrams
- Saving diagrams to files

Run:
```bash
bash examples/cli_usage.sh
```

## Quick Start

1. Install mdflow:
```bash
pip install -e .
```

2. Run any example from the project root:
```bash
python examples/basic_usage.py
```

3. Check the `output/` directory for generated reports and diagrams.

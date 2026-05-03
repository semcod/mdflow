# System Architecture Analysis

## Overview

- **Project**: /home/tom/github/semcod/mdflow
- **Primary Language**: python
- **Languages**: python: 20, md: 12, yaml: 11, shell: 4, txt: 2
- **Analysis Mode**: static
- **Total Functions**: 132
- **Total Classes**: 32
- **Modules**: 51
- **Entry Points**: 120

## Architecture by Module

### SUMD
- **Functions**: 50
- **Classes**: 9
- **File**: `SUMD.md`

### project.map.toon
- **Functions**: 33
- **File**: `map.toon.yaml`

### SUMR
- **Functions**: 17
- **Classes**: 9
- **File**: `SUMR.md`

### mdflow
- **Functions**: 12
- **Classes**: 1
- **File**: `__init__.py`

### mdflow.generators.mermaid
- **Functions**: 9
- **File**: `mermaid.py`

### mdflow.parser
- **Functions**: 7
- **Classes**: 1
- **File**: `parser.py`

### mdflow.analyzers
- **Functions**: 7
- **Classes**: 4
- **File**: `__init__.py`

### mdflow.cli
- **Functions**: 4
- **File**: `cli.py`

### mdflow.generators.html
- **Functions**: 3
- **File**: `html.py`

### mdflow.models
- **Functions**: 2
- **Classes**: 8
- **File**: `models.py`

### examples.custom_diagrams
- **Functions**: 1
- **File**: `custom_diagrams.py`

### examples.directory_scan
- **Functions**: 1
- **File**: `directory_scan.py`

### examples.advanced_analysis
- **Functions**: 1
- **File**: `advanced_analysis.py`

### examples.basic_usage
- **Functions**: 1
- **File**: `basic_usage.py`

### examples.advanced.01_directory_scan
- **Functions**: 1
- **File**: `01_directory_scan.py`

### examples.basic.02_generate_reports
- **Functions**: 1
- **File**: `02_generate_reports.py`

### examples.basic.01_parse_single_file
- **Functions**: 1
- **File**: `01_parse_single_file.py`

### examples.basic.03_diagrams_as_strings
- **Functions**: 1
- **File**: `03_diagrams_as_strings.py`

### examples.data.project_overview
- **Functions**: 1
- **File**: `project_overview.md`

### examples.data.api_reference
- **Functions**: 1
- **File**: `api_reference.md`

## Key Entry Points

Main execution flows into the system:

### examples.advanced_analysis.main
- **Calls**: MdFlow, flow.parse, README.print, README.print, README.print, flow.structure, README.print, README.print

### examples.custom_diagrams.main
- **Calls**: MdFlow, flow.parse, README.print, README.print, README.print, flow.diagrams, diagrams.items, README.print

### mdflow.parser.MdParser.parse_text
- **Calls**: raw.splitlines, enumerate, next, mdflow.parser._parse_metadata_section, MdDocument, self.FENCE_OPEN_RE.match, self.HEADING_RE.match, self.LINK_RE.finditer

### examples.directory_scan.main
- **Calls**: MdFlow, README.print, README.print, README.print, flow.parse_dir, README.print, README.print, README.print

### examples.basic_usage.main
- **Calls**: MdFlow, flow.parse, README.print, README.print, README.print, README.print, README.print, README.print

### examples.basic.01_parse_single_file.main
- **Calls**: MdFlow, flow.parse, README.print, README.print, README.print, README.print, README.print, README.print

### examples.advanced.02_toon_analysis.main
- **Calls**: MdFlow, flow.parse, README.print, README.print, flow.toon_metrics, README.print, README.print, README.print

### mdflow.cli.main
- **Calls**: argparse.ArgumentParser, parser.add_subparsers, sub.add_parser, p_analyze.add_argument, p_analyze.add_argument, p_analyze.add_argument, p_analyze.set_defaults, sub.add_parser

### mdflow.generators.mermaid.alerts_diagram
> Mermaid flowchart of TOON alerts and refactor recommendations.
- **Calls**: metrics.get, metrics.get, lines.append, lines.append, None.join, lines.append, lines.append, enumerate

### mdflow.cli.cmd_analyze
- **Calls**: MdFlow, flow.parse, README.print, README.print, README.print, README.print, README.print, README.print

### examples.advanced.03_custom_diagram_pipeline.main
- **Calls**: MdFlow, Path, out_path.parent.mkdir, out_path.write_text, README.print, README.print, README.print, flow.parse

### examples.advanced.01_directory_scan.main
- **Calls**: MdFlow, flow.scan, README.print, README.print, README.print, README.print, README.print, README.print

### examples.basic.03_diagrams_as_strings.main
- **Calls**: MdFlow, flow.parse, flow.diagrams, README.print, diagrams.items, README.print, README.print, README.print

### mdflow.generators.mermaid.section_flowchart
> Mermaid flowchart showing sections with their code/link counts.
- **Calls**: enumerate, None.join, lines.append, mdflow.generators.mermaid._short_label, None.join, annotations.append, annotations.append, annotations.append

### mdflow.cli.cmd_diagram
- **Calls**: MdFlow, flow.parse, flow.diagrams, README.print, README.print, sys.exit, README.print, Path

### mdflow.generators.mermaid.dependency_diagram
> Mermaid flowchart of cross-document dependencies.
- **Calls**: None.join, mdflow.generators.mermaid._safe_id, lines.append, mdflow.generators.mermaid._safe_id, mdflow.generators.mermaid._safe_id, edge_kinds.get, node.endswith, mdflow.generators.mermaid._short_label

### mdflow.generators.mermaid.markpact_graph
> Mermaid graph of markpact embedded file references.
- **Calls**: mdflow.generators.mermaid._safe_id, lines.append, lines.append, None.items, None.join, enumerate, lines.append, lines.append

### mdflow.MdFlow.report
> Generate reports for a single document.

formats can include: "html", "md", "mermaid"
Default: all three.
- **Calls**: Path, out.mkdir, Path, mdflow.generators.html.generate_html_report, p.write_text, written.append, README.print, mdflow.generators.markdown.generate_markdown_report

### examples.basic.02_generate_reports.main
- **Calls**: MdFlow, flow.parse, flow.report, README.print, README.print, flow.report, README.print, README.print

### mdflow.MdFlow.scan
> Parse all .md files in a directory, generate reports, and build a
cross-document dependency graph report.
- **Calls**: self.parse_dir, README.print, Path, self.dependency_graph, mm.dependency_diagram, self.report, p.write_text, README.print

### mdflow.MdFlow.diagrams
> Return all diagrams as strings (keyed by name) without writing files.
Useful for embedding in other tools.
- **Calls**: self._struct.heading_tree, self._struct.section_summary, self._code_inv.inventory, self._toon.metrics, mm.heading_tree_diagram, mm.section_flowchart, mm.code_inventory_pie, mm.markpact_graph

### mdflow.generators.mermaid.workflow_diagram
> Extract workflow steps from DOQL/CSS code blocks and render as flowchart.
- **Calls**: re.compile, re.compile, wf_re.findall, None.join, mdflow.generators.mermaid._safe_id, lines.append, len, lines.append

### mdflow.analyzers.StructureAnalyzer.section_summary
> List of sections with code block count, link count, list item count.
- **Calls**: enumerate, sections.append, float, len, len, list, len, len

### mdflow.analyzers.ToonAnalyzer.metrics
- **Calls**: ts.name.upper, self.CC_RE.search, self.CRITICAL_RE.search, float, int, m.group, m.group, self._parse_health

### mdflow.analyzers.DependencyAnalyzer.build
- **Calls**: DependencyGraph, g.add_node, self._resolve_path, g.add_edge, g.add_edge, DependencyEdge, DependencyEdge

### mdflow.analyzers.CodeInventoryAnalyzer.inventory
- **Calls**: defaultdict, defaultdict, None.append, len, dict, dict, None.append

### mdflow.cli.cmd_scan
- **Calls**: MdFlow, flow.scan, README.print, args.format.split, len, len

### mdflow.analyzers.ToonAnalyzer._parse_health
- **Calls**: self.CC_RE.search, self.CRITICAL_RE.search, float, int, m.group, m.group

### mdflow.MdFlow.parse_dir
> Parse all .md files in a directory tree.
- **Calls**: Path, sorted, root.rglob, docs.append, self._parser.parse, README.print

### mdflow.MdFlow._write_dep_graph_html
- **Calls**: None.replace, p.write_text, README.print, diagram.replace, len, len

## Process Flows

Key execution flows identified:

### Flow 1: main
```
main [examples.advanced_analysis]
  └─ →> print
  └─ →> print
```

### Flow 2: parse_text
```
parse_text [mdflow.parser.MdParser]
  └─ →> _parse_metadata_section
```

### Flow 3: alerts_diagram
```
alerts_diagram [mdflow.generators.mermaid]
```

### Flow 4: cmd_analyze
```
cmd_analyze [mdflow.cli]
  └─ →> print
  └─ →> print
```

### Flow 5: section_flowchart
```
section_flowchart [mdflow.generators.mermaid]
  └─> _short_label
```

### Flow 6: cmd_diagram
```
cmd_diagram [mdflow.cli]
  └─ →> print
  └─ →> print
```

### Flow 7: dependency_diagram
```
dependency_diagram [mdflow.generators.mermaid]
  └─> _safe_id
  └─> _safe_id
```

### Flow 8: markpact_graph
```
markpact_graph [mdflow.generators.mermaid]
  └─> _safe_id
```

### Flow 9: report
```
report [mdflow.MdFlow]
  └─ →> generate_html_report
      └─> _card
```

### Flow 10: scan
```
scan [mdflow.MdFlow]
  └─ →> print
```

## Key Classes

### mdflow.MdFlow
> High-level façade for the mdflow library.

Examples
--------
Single file:
    flow = MdFlow()
    do
- **Methods**: 12
- **Key Methods**: mdflow.MdFlow.__init__, mdflow.MdFlow.parse, mdflow.MdFlow.parse_dir, mdflow.MdFlow.dependency_graph, mdflow.MdFlow.structure, mdflow.MdFlow.code_inventory, mdflow.MdFlow.toon_metrics, mdflow.MdFlow.report, mdflow.MdFlow.scan, mdflow.MdFlow.diagrams

### mdflow.models.MdDocument
> Full parsed representation of one Markdown file.
- **Methods**: 4
- **Key Methods**: mdflow.models.MdDocument.internal_links, mdflow.models.MdDocument.anchor_links, mdflow.models.MdDocument.external_links, mdflow.models.MdDocument.markpact_blocks

### mdflow.parser.MdParser
> Parse a single Markdown file into an MdDocument.
- **Methods**: 2
- **Key Methods**: mdflow.parser.MdParser.parse, mdflow.parser.MdParser.parse_text

### mdflow.models.DependencyGraph
- **Methods**: 2
- **Key Methods**: mdflow.models.DependencyGraph.add_node, mdflow.models.DependencyGraph.add_edge

### mdflow.analyzers.DependencyAnalyzer
> Build a cross-document dependency graph from a list of MdDocuments.
- **Methods**: 2
- **Key Methods**: mdflow.analyzers.DependencyAnalyzer.build, mdflow.analyzers.DependencyAnalyzer._resolve_path

### mdflow.analyzers.StructureAnalyzer
> Analyse the heading/section structure of a single document.
- **Methods**: 2
- **Key Methods**: mdflow.analyzers.StructureAnalyzer.heading_tree, mdflow.analyzers.StructureAnalyzer.section_summary

### mdflow.analyzers.ToonAnalyzer
> Extract structured metrics from embedded TOON sections.
- **Methods**: 2
- **Key Methods**: mdflow.analyzers.ToonAnalyzer.metrics, mdflow.analyzers.ToonAnalyzer._parse_health

### mdflow.analyzers.CodeInventoryAnalyzer
> Inventory all code blocks by language, markpact type, and path.
- **Methods**: 1
- **Key Methods**: mdflow.analyzers.CodeInventoryAnalyzer.inventory

### mdflow.models.Heading
- **Methods**: 0

### mdflow.models.Link
- **Methods**: 0

### mdflow.models.CodeBlock
- **Methods**: 0

### mdflow.models.ListItem
- **Methods**: 0

### mdflow.models.ToonSection
> A named TOON/YAML embedded block (from code blocks with toon language).
- **Methods**: 0

### mdflow.models.DependencyEdge
- **Methods**: 0

### SUMD.MdParser
- **Methods**: 0

### SUMD.Heading
- **Methods**: 0

### SUMD.Link
- **Methods**: 0

### SUMD.CodeBlock
- **Methods**: 0

### SUMD.ListItem
- **Methods**: 0

### SUMD.ToonSection
- **Methods**: 0

## Data Transformation Functions

Key functions that process and transform data:

### examples.data.project_overview.process_data

### mdflow.parser._parse_fence_info
> Parse fence info string like:
  python
  toon markpact:analysis path=project/evolution.toon.yaml
  c
- **Output to**: None.split, part.startswith, info.strip, part.split, part.split

### mdflow.parser._parse_toon_content
> Lightly parse TOON format embedded in code blocks.
- **Output to**: content.splitlines, _TOON_SECTION_RE.match, sections.append, m.group, _TOON_ITEM_RE.match

### mdflow.parser._parse_metadata_section
> Extract key/value pairs from a ## Metadata list section.
- **Output to**: text.splitlines, re.match, re.match, _META_ITEM_RE.match, None.strip

### mdflow.parser.MdParser.parse
- **Output to**: Path, path.read_text, self.parse_text, str

### mdflow.parser.MdParser.parse_text
- **Output to**: raw.splitlines, enumerate, next, mdflow.parser._parse_metadata_section, MdDocument

### mdflow.analyzers.ToonAnalyzer._parse_health
- **Output to**: self.CC_RE.search, self.CRITICAL_RE.search, float, int, m.group

### SUMD._parse_fence_info

### SUMD._parse_toon_content

### SUMD._parse_metadata_section

### SUMD.parse

### SUMD.parse_text

### project.map.toon._parse_fence_info

### project.map.toon._parse_toon_content

### project.map.toon._parse_metadata_section

### SUMR._parse_fence_info

### SUMR._parse_toon_content

### SUMR._parse_metadata_section

### SUMR.parse

### SUMR.parse_text

### mdflow.MdFlow.parse
> Parse a single Markdown file into an MdDocument.
- **Output to**: self._parser.parse, Path

### mdflow.MdFlow.parse_dir
> Parse all .md files in a directory tree.
- **Output to**: Path, sorted, root.rglob, docs.append, self._parser.parse

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `examples.advanced_analysis.main` - 57 calls
- `mdflow.generators.html.generate_html_report` - 54 calls
- `examples.custom_diagrams.main` - 40 calls
- `mdflow.parser.MdParser.parse_text` - 40 calls
- `examples.directory_scan.main` - 39 calls
- `examples.basic_usage.main` - 35 calls
- `mdflow.generators.markdown.generate_markdown_report` - 33 calls
- `examples.basic.01_parse_single_file.main` - 31 calls
- `examples.advanced.02_toon_analysis.main` - 25 calls
- `mdflow.cli.main` - 19 calls
- `mdflow.generators.mermaid.alerts_diagram` - 19 calls
- `mdflow.cli.cmd_analyze` - 17 calls
- `examples.advanced.03_custom_diagram_pipeline.main` - 17 calls
- `examples.advanced.01_directory_scan.main` - 15 calls
- `examples.basic.03_diagrams_as_strings.main` - 15 calls
- `mdflow.generators.mermaid.section_flowchart` - 14 calls
- `mdflow.cli.cmd_diagram` - 13 calls
- `mdflow.generators.mermaid.dependency_diagram` - 12 calls
- `mdflow.generators.mermaid.markpact_graph` - 12 calls
- `mdflow.MdFlow.report` - 12 calls
- `examples.basic.02_generate_reports.main` - 10 calls
- `mdflow.MdFlow.scan` - 10 calls
- `mdflow.MdFlow.diagrams` - 10 calls
- `mdflow.generators.mermaid.workflow_diagram` - 9 calls
- `mdflow.analyzers.StructureAnalyzer.section_summary` - 8 calls
- `mdflow.analyzers.ToonAnalyzer.metrics` - 8 calls
- `mdflow.analyzers.DependencyAnalyzer.build` - 7 calls
- `mdflow.analyzers.CodeInventoryAnalyzer.inventory` - 7 calls
- `mdflow.cli.cmd_scan` - 6 calls
- `mdflow.MdFlow.parse_dir` - 6 calls
- `mdflow.generators.mermaid.heading_tree_diagram` - 5 calls
- `mdflow.parser.MdParser.parse` - 4 calls
- `mdflow.generators.mermaid.code_inventory_pie` - 4 calls
- `mdflow.analyzers.StructureAnalyzer.heading_tree` - 4 calls
- `mdflow.models.DependencyGraph.add_edge` - 3 calls
- `mdflow.MdFlow.parse` - 2 calls
- `mdflow.MdFlow.structure` - 2 calls
- `mdflow.models.DependencyGraph.add_node` - 1 calls
- `mdflow.MdFlow.dependency_graph` - 1 calls
- `mdflow.MdFlow.code_inventory` - 1 calls

## System Interactions

How components interact:

```mermaid
graph TD
    main --> MdFlow
    main --> parse
    main --> print
    parse_text --> splitlines
    parse_text --> enumerate
    parse_text --> next
    parse_text --> _parse_metadata_sect
    parse_text --> MdDocument
    main --> parse_dir
    main --> toon_metrics
    main --> ArgumentParser
    main --> add_subparsers
    main --> add_parser
    main --> add_argument
    alerts_diagram --> get
    alerts_diagram --> append
    alerts_diagram --> join
    cmd_analyze --> MdFlow
    cmd_analyze --> parse
    cmd_analyze --> print
    main --> Path
    main --> mkdir
    main --> write_text
    main --> scan
    main --> diagrams
    main --> items
    section_flowchart --> enumerate
    section_flowchart --> join
    section_flowchart --> append
    section_flowchart --> _short_label
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.
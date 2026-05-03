#!/usr/bin/env python3
"""
Example: Use MdParser directly for low-level control.

MdFlow is a convenience facade. For fine-grained control, use MdParser
and the data models directly.

Run from project root:
    python examples/api/01_low_level_parser.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow.parser import MdParser


def main():
    parser = MdParser()

    # Parse a file
    doc = parser.parse("examples/data/project_overview.md")

    print(f"Title: {doc.title}")
    print(f"Path : {doc.path}")

    # Inspect code blocks in detail
    print("\n--- Code blocks ---")
    for cb in doc.code_blocks:
        print(f"\n  Language : {cb.language or '(none)'}")
        print(f"  Lines    : {cb.line_start}-{cb.line_end}")
        print(f"  Size     : {len(cb.content)} chars")

        if cb.markpact_type:
            print(f"  Markpact : {cb.markpact_type}")
        if cb.markpact_path:
            print(f"  Path     : {cb.markpact_path}")
        if cb.tags:
            print(f"  Tags     : {cb.tags}")

    # Inspect links with full detail
    print("\n--- Links ---")
    for link in doc.links:
        print(f"  [{link.text}] -> {link.href}  (kind={link.kind}, line={link.line})")

    # Parse raw text without a file
    raw_md = """
# Inline Document

Some text with a [link](https://example.com).

```python
x = 42
```

- Item one
- Item two
  - Nested item
"""
    inline_doc = parser.parse_text(raw_md, path="<inline>")
    print(f"\n--- Inline doc ---")
    print(f"  Title      : {inline_doc.title}")
    print(f"  Headings   : {len(inline_doc.headings)}")
    print(f"  Links      : {len(inline_doc.links)}")
    print(f"  Code blocks: {len(inline_doc.code_blocks)}")
    print(f"  List items : {len(inline_doc.list_items)}")


if __name__ == "__main__":
    main()

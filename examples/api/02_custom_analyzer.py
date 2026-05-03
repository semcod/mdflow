#!/usr/bin/env python3
"""
Example: Build a custom analyzer using mdflow data models.

Demonstrates how to extend mdflow with your own analysis logic
using the parsed MdDocument structure.

Run from project root:
    python examples/api/02_custom_analyzer.py
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mdflow import MdFlow


def analyze_document(doc):
    """Custom analysis: count words per section, find dead links, etc."""
    results = {}

    # Word frequency in list items
    words = []
    for li in doc.list_items:
        words.extend(li.text.lower().split())
    results["top_words"] = Counter(words).most_common(10)

    # Code language distribution
    langs = Counter(cb.language for cb in doc.code_blocks if cb.language)
    results["languages"] = dict(langs)

    # Estimate reading sections (by heading count)
    results["sections"] = len(doc.headings)
    results["max_depth"] = max((h.level for h in doc.headings), default=0)

    # Links to images vs text
    images = [l for l in doc.links if l.kind == "image"]
    results["image_links"] = len(images)

    # Markpact coverage
    mp_types = Counter(cb.markpact_type for cb in doc.markpact_blocks)
    results["markpact_types"] = dict(mp_types)

    return results


def main():
    flow = MdFlow()

    doc = flow.parse("examples/data/project_overview.md")
    stats = analyze_document(doc)

    print(f"Custom analysis for: {doc.title}")
    print("=" * 60)

    print(f"\nDocument structure:")
    print(f"  Sections   : {stats['sections']}")
    print(f"  Max depth  : H{stats['max_depth']}")

    print(f"\nTop words in list items:")
    for word, count in stats["top_words"]:
        print(f"  {word:20s}: {count}")

    print(f"\nCode languages:")
    for lang, count in stats["languages"].items():
        print(f"  {lang:15s}: {count}")

    print(f"\nImage links: {stats['image_links']}")

    if stats["markpact_types"]:
        print(f"\nMarkpact types:")
        for mp_type, count in stats["markpact_types"].items():
            print(f"  {mp_type:15s}: {count}")


if __name__ == "__main__":
    main()

"""
mdflow.models — core data structures for Markdown dependency analysis.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Heading:
    level: int  # 1–6
    text: str
    anchor: str  # slug-ified, e.g. "source-map"
    line: int


@dataclass
class Link:
    text: str
    href: str
    line: int
    kind: str  # "internal", "external", "anchor", "image"


@dataclass
class CodeBlock:
    language: str  # e.g. "python", "toon", "css", "yaml"
    content: str
    line_start: int
    line_end: int
    # markpact metadata, e.g. markpact:doql path=app.doql.css
    markpact_type: Optional[str] = None
    markpact_path: Optional[str] = None
    # additional tags parsed from the fence info string
    tags: dict = field(default_factory=dict)


@dataclass
class ListItem:
    text: str
    line: int
    depth: int  # nesting level (0 = top)
    parent_heading: Optional[str] = None


@dataclass
class ToonSection:
    """A named TOON/YAML embedded block (from code blocks with toon language)."""

    name: str  # e.g. "REFACTOR", "ALERTS", "HOTSPOTS"
    items: list  # raw parsed items
    source_block: Optional[CodeBlock] = None


@dataclass
class MdDocument:
    """Full parsed representation of one Markdown file."""

    path: str
    title: str
    headings: list[Heading] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    code_blocks: list[CodeBlock] = field(default_factory=list)
    list_items: list[ListItem] = field(default_factory=list)
    toon_sections: list[ToonSection] = field(default_factory=list)
    # extracted from metadata section
    metadata: dict = field(default_factory=dict)
    raw: str = ""

    @property
    def internal_links(self) -> list[Link]:
        return [lk for lk in self.links if lk.kind == "internal"]

    @property
    def anchor_links(self) -> list[Link]:
        return [lk for lk in self.links if lk.kind == "anchor"]

    @property
    def external_links(self) -> list[Link]:
        return [lk for lk in self.links if lk.kind == "external"]

    @property
    def markpact_blocks(self) -> list[CodeBlock]:
        return [b for b in self.code_blocks if b.markpact_type]


@dataclass
class DependencyEdge:
    source: str  # document path or heading anchor
    target: str
    kind: str  # "link", "import", "embed", "references"
    label: str = ""


@dataclass
class DependencyGraph:
    nodes: list[str] = field(default_factory=list)
    edges: list[DependencyEdge] = field(default_factory=list)

    def add_node(self, node: str):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, edge: DependencyEdge):
        self.add_node(edge.source)
        self.add_node(edge.target)
        self.edges.append(edge)

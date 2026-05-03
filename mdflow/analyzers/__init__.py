"""
mdflow.analyzers — build dependency graphs and structural analysis
from one or more parsed MdDocuments.
"""

from __future__ import annotations
import re
from collections import defaultdict
from pathlib import Path
from ..models import MdDocument, DependencyEdge, DependencyGraph


# ─── dependency graph ─────────────────────────────────────────────────────────


class DependencyAnalyzer:
    """Build a cross-document dependency graph from a list of MdDocuments."""

    def build(self, docs: list[MdDocument]) -> DependencyGraph:
        g = DependencyGraph()
        path_set = {d.path for d in docs}

        for doc in docs:
            g.add_node(doc.path)

            # 1. Internal file links
            for link in doc.internal_links:
                target = self._resolve_path(doc.path, link.href)
                if target in path_set:
                    g.add_edge(
                        DependencyEdge(
                            source=doc.path,
                            target=target,
                            kind="link",
                            label=link.text or link.href,
                        )
                    )

            # 2. markpact embedded file references
            for cb in doc.markpact_blocks:
                if cb.markpact_path:
                    g.add_edge(
                        DependencyEdge(
                            source=doc.path,
                            target=cb.markpact_path,
                            kind="embed",
                            label=f"markpact:{cb.markpact_type}",
                        )
                    )

        return g

    def _resolve_path(self, base_path: str, href: str) -> str:
        base = Path(base_path).parent
        resolved = (base / href).resolve()
        # Keep relative if original base_path was relative, for consistent path_set matching
        try:
            return str(resolved.relative_to(Path.cwd()))
        except ValueError:
            return str(resolved)


# ─── section structure ────────────────────────────────────────────────────────


class StructureAnalyzer:
    """Analyse the heading/section structure of a single document."""

    def heading_tree(self, doc: MdDocument) -> list[dict]:
        """Return a nested tree of headings."""
        tree: list[dict] = []
        stack: list[dict] = []

        for h in doc.headings:
            node = {
                "level": h.level,
                "text": h.text,
                "anchor": h.anchor,
                "children": [],
            }
            while stack and stack[-1]["level"] >= h.level:
                stack.pop()
            if stack:
                stack[-1]["children"].append(node)
            else:
                tree.append(node)
            stack.append(node)

        return tree

    def _section_for_heading(self, h, next_line: float, doc: MdDocument) -> dict:
        cbs = [cb for cb in doc.code_blocks if h.line <= cb.line_start < next_line]
        lks = [lk for lk in doc.links if h.line <= lk.line < next_line]
        lis = [li for li in doc.list_items if h.line <= li.line < next_line]
        return {
            "heading": h.text,
            "level": h.level,
            "anchor": h.anchor,
            "code_blocks": len(cbs),
            "languages": list({cb.language for cb in cbs if cb.language}),
            "links": len(lks),
            "list_items": len(lis),
            "markpact": [cb.markpact_type for cb in cbs if cb.markpact_type],
        }

    def section_summary(self, doc: MdDocument) -> list[dict]:
        """List of sections with code block count, link count, list item count."""
        headings = [h for h in doc.headings if h.level <= 3]
        return [
            self._section_for_heading(
                h,
                headings[i + 1].line if i + 1 < len(headings) else float("inf"),
                doc,
            )
            for i, h in enumerate(headings)
        ]


# ─── code block inventory ─────────────────────────────────────────────────────


class CodeInventoryAnalyzer:
    """Inventory all code blocks by language, markpact type, and path."""

    def inventory(self, doc: MdDocument) -> dict:
        by_lang: dict = defaultdict(list)
        by_markpact: dict = defaultdict(list)

        for cb in doc.code_blocks:
            by_lang[cb.language or "unknown"].append(
                {
                    "lines": cb.line_end - cb.line_start,
                    "markpact": cb.markpact_type,
                    "path": cb.markpact_path,
                    "line_start": cb.line_start,
                }
            )
            if cb.markpact_type:
                by_markpact[cb.markpact_type].append(
                    {
                        "path": cb.markpact_path,
                        "language": cb.language,
                        "line_start": cb.line_start,
                    }
                )

        return {
            "total": len(doc.code_blocks),
            "by_language": dict(by_lang),
            "by_markpact": dict(by_markpact),
            "markpact_paths": [
                cb.markpact_path for cb in doc.code_blocks if cb.markpact_path
            ],
        }


# ─── toon metrics ─────────────────────────────────────────────────────────────


class ToonAnalyzer:
    """Extract structured metrics from embedded TOON sections."""

    # Patterns for common TOON metrics
    CC_RE = re.compile(r"CC[=̄]\s*([\d.]+)")
    CRITICAL_RE = re.compile(r"critical\s*[=:]\s*(\d+)")
    DUP_RE = re.compile(r"dup\s*[=:]\s*(\d+)")

    def metrics(self, doc: MdDocument) -> dict:
        result: dict = {
            "toon_sections": [ts.name for ts in doc.toon_sections],
            "alerts": [],
            "refactors": [],
            "hotspots": [],
            "health": {},
        }

        for ts in doc.toon_sections:
            name = ts.name.upper()
            if name in ("ALERTS", "ALERT"):
                result["alerts"] = ts.items
            elif name in ("REFACTOR",):
                result["refactors"] = ts.items
            elif name in ("HOTSPOTS", "HOTSPOT"):
                result["hotspots"] = ts.items
            elif name in ("HEALTH",):
                result["health"] = self._parse_health(ts)

        # Try to extract CC from raw code block content
        for cb in doc.code_blocks:
            if cb.language in ("toon", "yaml") or (cb.markpact_type == "analysis"):
                m = self.CC_RE.search(cb.content)
                if m:
                    result["health"]["cc_mean"] = float(m.group(1))
                m = self.CRITICAL_RE.search(cb.content)
                if m:
                    result["health"]["critical"] = int(m.group(1))

        return result

    def _parse_health(self, ts) -> dict:
        health: dict = {}
        for item in ts.items:
            m = self.CC_RE.search(item)
            if m:
                health["cc_mean"] = float(m.group(1))
            m = self.CRITICAL_RE.search(item)
            if m:
                health["critical"] = int(m.group(1))
        return health

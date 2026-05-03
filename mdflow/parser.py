"""
mdflow.parser — core Markdown parser.

Extracts: headings, links, code blocks (with markpact metadata),
list items, TOON sections, and document metadata.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Optional
from .models import Heading, Link, CodeBlock, ListItem, ToonSection, MdDocument


# ─── helpers ──────────────────────────────────────────────────────────────────


def _slugify(text: str) -> str:
    """GitHub-style anchor slugification."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text.strip())
    return text


def _classify_link(href: str) -> str:
    if href.startswith("#"):
        return "anchor"
    if href.startswith("http://") or href.startswith("https://"):
        return "external"
    if href.endswith((".png", ".jpg", ".gif", ".svg", ".webp")):
        return "image"
    return "internal"


def _parse_fence_info(info: str) -> tuple[str, Optional[str], Optional[str], dict]:
    """
    Parse fence info string like:
      python
      toon markpact:analysis path=project/evolution.toon.yaml
      css markpact:doql path=app.doql.css
    Returns (language, markpact_type, markpact_path, extra_tags)
    """
    parts = info.strip().split()
    if not parts:
        return "", None, None, {}

    language = parts[0]
    markpact_type = None
    markpact_path = None
    tags: dict = {}

    for part in parts[1:]:
        if part.startswith("markpact:"):
            markpact_type = part.split(":", 1)[1]
        elif "=" in part:
            k, v = part.split("=", 1)
            tags[k] = v
            if k == "path":
                markpact_path = v
        else:
            tags[part] = True

    return language, markpact_type, markpact_path, tags


# ─── TOON section parser ───────────────────────────────────────────────────────

_TOON_SECTION_RE = re.compile(r"^([A-Z_]+)\[(\d+)\]")
_TOON_ITEM_RE = re.compile(r"^\s+\[(\d+)\]\s+(.+)")
_TOON_ALERT_RE = re.compile(r"^\s+[!★]\s+(.+)")


def _parse_toon_content(content: str) -> list[ToonSection]:
    """Lightly parse TOON format embedded in code blocks."""
    sections: list[ToonSection] = []
    current_name = None
    current_items: list = []

    for line in content.splitlines():
        m = _TOON_SECTION_RE.match(line)
        if m:
            if current_name:
                sections.append(ToonSection(name=current_name, items=current_items))
            current_name = m.group(1)
            current_items = []
            continue

        if current_name:
            item_m = _TOON_ITEM_RE.match(line)
            if item_m:
                current_items.append(item_m.group(2).strip())
                continue
            alert_m = _TOON_ALERT_RE.match(line)
            if alert_m:
                current_items.append(alert_m.group(1).strip())

    if current_name:
        sections.append(ToonSection(name=current_name, items=current_items))

    return sections


# ─── metadata section parser ───────────────────────────────────────────────────

_META_ITEM_RE = re.compile(r"^\s*-\s+\*\*(.+?)\*\*:\s*`?(.+?)`?\s*$")


def _parse_metadata_section(text: str) -> dict:
    """Extract key/value pairs from a ## Metadata list section."""
    meta: dict = {}
    in_meta = False
    for line in text.splitlines():
        if re.match(r"^##\s+Metadata", line):
            in_meta = True
            continue
        if in_meta and re.match(r"^##\s+", line):
            break
        if in_meta:
            m = _META_ITEM_RE.match(line)
            if m:
                meta[m.group(1).strip()] = m.group(2).strip()
    return meta


# ─── main parser ──────────────────────────────────────────────────────────────


class MdParser:
    """Parse a single Markdown file into an MdDocument."""

    HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
    LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
    LIST_RE = re.compile(r"^(\s*)[-*+]\s+(.+)$")
    FENCE_OPEN_RE = re.compile(r"^```(.*)$")
    FENCE_CLOSE_RE = re.compile(r"^```\s*$")

    def parse(self, path: str | Path) -> MdDocument:
        path = Path(path)
        raw = path.read_text(encoding="utf-8")
        return self.parse_text(raw, str(path))

    def parse_text(self, raw: str, path: str = "<string>") -> MdDocument:
        lines = raw.splitlines()
        headings: list[Heading] = []
        links: list[Link] = []
        code_blocks: list[CodeBlock] = []
        list_items: list[ListItem] = []
        toon_sections: list[ToonSection] = []

        in_fence = False
        fence_info = ""
        fence_start = 0
        fence_lines: list[str] = []
        current_heading: Optional[str] = None

        for lineno, line in enumerate(lines, start=1):
            # ── fence handling ────────────────────────────────────────────────
            if in_fence:
                if self.FENCE_CLOSE_RE.match(line):
                    content = "\n".join(fence_lines)
                    lang, mp_type, mp_path, tags = _parse_fence_info(fence_info)
                    cb = CodeBlock(
                        language=lang,
                        content=content,
                        line_start=fence_start,
                        line_end=lineno,
                        markpact_type=mp_type,
                        markpact_path=mp_path,
                        tags=tags,
                    )
                    code_blocks.append(cb)

                    # Parse TOON sections from toon/yaml blocks
                    if lang in ("toon", "yaml") or mp_type == "analysis":
                        for ts in _parse_toon_content(content):
                            ts.source_block = cb
                            toon_sections.append(ts)

                    in_fence = False
                    fence_lines = []
                else:
                    fence_lines.append(line)
                continue

            fence_m = self.FENCE_OPEN_RE.match(line)
            if fence_m:
                in_fence = True
                fence_info = fence_m.group(1)
                fence_start = lineno
                fence_lines = []
                continue

            # ── headings ─────────────────────────────────────────────────────
            h_m = self.HEADING_RE.match(line)
            if h_m:
                level = len(h_m.group(1))
                text = h_m.group(2).strip()
                anchor = _slugify(text)
                h = Heading(level=level, text=text, anchor=anchor, line=lineno)
                headings.append(h)
                current_heading = anchor
                continue

            # ── links (outside code blocks) ───────────────────────────────────
            for m in self.LINK_RE.finditer(line):
                full = m.group(0)
                is_image = full.startswith("!")
                text = m.group(1)
                href = m.group(2)
                kind = "image" if is_image else _classify_link(href)
                links.append(Link(text=text, href=href, line=lineno, kind=kind))

            # ── list items ────────────────────────────────────────────────────
            l_m = self.LIST_RE.match(line)
            if l_m:
                depth = len(l_m.group(1)) // 2
                text = l_m.group(2).strip()
                # strip inline backticks/bold
                text_clean = re.sub(r"[`*_]", "", text)
                list_items.append(
                    ListItem(
                        text=text_clean,
                        line=lineno,
                        depth=depth,
                        parent_heading=current_heading,
                    )
                )

        # ── title = first H1 ─────────────────────────────────────────────────
        title = next((h.text for h in headings if h.level == 1), Path(path).stem)

        # ── metadata ─────────────────────────────────────────────────────────
        metadata = _parse_metadata_section(raw)

        return MdDocument(
            path=path,
            title=title,
            headings=headings,
            links=links,
            code_blocks=code_blocks,
            list_items=list_items,
            toon_sections=toon_sections,
            metadata=metadata,
            raw=raw,
        )

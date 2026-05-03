"""
mdflow.validators — validate generated Mermaid diagrams and report issues
as planfile-compatible TODO tickets.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date


# ─── known Mermaid structural patterns ───────────────────────────────────────

_DIAGRAM_TYPES = re.compile(
    r"^(flowchart|graph|sequenceDiagram|classDiagram|stateDiagram"
    r"|erDiagram|gantt|pie|mindmap|timeline|gitGraph|xychart-beta)\b",
    re.MULTILINE,
)
_UNESCAPED_QUOTE = re.compile(r'(?<!\\)"[^"]*"[^"]*"')
_BROKEN_NODE_ID = re.compile(r"\b([A-Za-z0-9_]+)\s*\[\"[^\"]*[`()\[\]{}][^\"]*\"\]")
_EMPTY_LABEL = re.compile(r'\[""\]|\["\\n')
_DUPLICATE_NODE = re.compile(r"^\s{0,4}([A-Za-z0-9_]+)\[", re.MULTILINE)


@dataclass
class ValidationIssue:
    diagram_name: str
    file_path: str
    severity: str  # "error" | "warning"
    code: str  # short machine-readable code
    message: str
    line: int = 0


@dataclass
class ValidationResult:
    diagram_name: str
    file_path: str
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)


def _check_has_diagram_type(
    name: str, path: str, content: str
) -> list[ValidationIssue]:
    if not _DIAGRAM_TYPES.search(content):
        return [
            ValidationIssue(
                diagram_name=name,
                file_path=path,
                severity="error",
                code="NO_DIAGRAM_TYPE",
                message="Diagram has no recognisable Mermaid type keyword",
            )
        ]
    return []


def _check_empty(name: str, path: str, content: str) -> list[ValidationIssue]:
    stripped = content.strip()
    if not stripped:
        return [
            ValidationIssue(
                diagram_name=name,
                file_path=path,
                severity="error",
                code="EMPTY_DIAGRAM",
                message="Diagram is empty",
            )
        ]
    if len(stripped.splitlines()) < 2:
        return [
            ValidationIssue(
                diagram_name=name,
                file_path=path,
                severity="warning",
                code="TRIVIAL_DIAGRAM",
                message="Diagram has only one line (likely no content nodes)",
            )
        ]
    return []


def _check_broken_labels(name: str, path: str, content: str) -> list[ValidationIssue]:
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        # backtick inside quoted label
        if '"`' in line or '`"' in line:
            issues.append(
                ValidationIssue(
                    diagram_name=name,
                    file_path=path,
                    line=i,
                    severity="error",
                    code="BACKTICK_IN_LABEL",
                    message=f"Backtick inside node label (line {i}): {line.strip()[:60]}",
                )
            )
        # unbalanced double-quotes in a label string
        label_match = re.search(r'\["([^"\\]|\\.)*"\]', line)
        if not label_match and "[" in line and '"' in line:
            issues.append(
                ValidationIssue(
                    diagram_name=name,
                    file_path=path,
                    line=i,
                    severity="warning",
                    code="SUSPECT_LABEL",
                    message=f"Possibly malformed node label (line {i}): {line.strip()[:60]}",
                )
            )
    return issues


def _check_duplicate_ids(name: str, path: str, content: str) -> list[ValidationIssue]:
    seen: dict[str, int] = {}
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        m = re.match(r"^\s{0,6}([A-Za-z][A-Za-z0-9_]*)\[", line)
        if m:
            nid = m.group(1)
            if nid in seen:
                issues.append(
                    ValidationIssue(
                        diagram_name=name,
                        file_path=path,
                        line=i,
                        severity="warning",
                        code="DUPLICATE_NODE_ID",
                        message=f"Node id '{nid}' defined again (first at line {seen[nid]})",
                    )
                )
            else:
                seen[nid] = i
    return issues


def _check_mindmap(name: str, path: str, content: str) -> list[ValidationIssue]:
    if not content.startswith("mindmap"):
        return []
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if (
            stripped
            and not stripped.startswith("root")
            and not stripped.startswith("mindmap")
        ):
            # Illegal characters in mindmap node text
            if re.search(r'["`()\[\]{}]', stripped):
                issues.append(
                    ValidationIssue(
                        diagram_name=name,
                        file_path=path,
                        line=i,
                        severity="error",
                        code="MINDMAP_ILLEGAL_CHARS",
                        message=f"Illegal characters in mindmap node (line {i}): {stripped[:60]}",
                    )
                )
    return issues


def validate_diagram(name: str, path: str, content: str) -> ValidationResult:
    """Run all checks on a single diagram string."""
    issues: list[ValidationIssue] = []
    issues += _check_empty(name, path, content)
    if not issues:  # skip further checks if empty
        issues += _check_has_diagram_type(name, path, content)
        issues += _check_broken_labels(name, path, content)
        issues += _check_duplicate_ids(name, path, content)
        issues += _check_mindmap(name, path, content)
    has_errors = any(i.severity == "error" for i in issues)
    return ValidationResult(
        diagram_name=name,
        file_path=path,
        valid=not has_errors,
        issues=issues,
    )


def validate_mermaid_files(paths: list[Path]) -> list[ValidationResult]:
    """Validate a list of .mermaid files on disk."""
    results = []
    for p in paths:
        content = p.read_text(encoding="utf-8") if p.exists() else ""
        results.append(validate_diagram(p.stem.split("_", 1)[-1], str(p), content))
    return results


# ─── TODO.md / planfile ticket writer ────────────────────────────────────────


def _ticket_id(issue: ValidationIssue) -> str:
    safe = re.sub(r"[^A-Z0-9_]", "_", issue.code.upper())
    safe_name = re.sub(r"[^A-Z0-9]", "", issue.diagram_name.upper())[:8]
    return f"MERMAID-{safe_name}-{safe}"


def write_todo_tickets(results: list[ValidationResult], todo_path: Path) -> int:
    """
    Append planfile-compatible TODO tickets for any failed diagram validation.
    Returns the number of new tickets written.
    """
    failing = [r for r in results if not r.valid]
    if not failing:
        return 0

    existing = todo_path.read_text(encoding="utf-8") if todo_path.exists() else ""
    today = date.today().isoformat()
    new_tickets: list[str] = []

    for result in failing:
        for issue in result.issues:
            if issue.severity != "error":
                continue
            tid = _ticket_id(issue)
            if tid in existing:
                continue  # already reported, skip
            ticket = (
                f"\n## [{tid}] {issue.code}: {result.diagram_name}\n"
                f"- **date**: {today}\n"
                f"- **severity**: {issue.severity}\n"
                f"- **file**: `{issue.file_path}`\n"
                f"- **line**: {issue.line or 'n/a'}\n"
                f"- **message**: {issue.message}\n"
                f"- **status**: open\n"
            )
            new_tickets.append(ticket)

    if not new_tickets:
        return 0

    header = "# mdflow — Diagram Validation Issues\n" if not existing.strip() else ""
    todo_path.write_text(existing + header + "".join(new_tickets), encoding="utf-8")
    return len(new_tickets)

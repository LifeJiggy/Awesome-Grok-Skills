"""
Technical Documentation Authoring & Lifecycle Management

Provides style guide enforcement, cross-reference integrity checking,
multi-format rendering, content lifecycle tracking, terminology management,
and documentation site generation.
"""

from __future__ import annotations

import re
import os
import hashlib
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ContentFormat(Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    ASCIIDOC = "asciidoc"


class OutputFormat(Enum):
    HTML = "html"
    PDF = "pdf"
    ASCIIDOC = "asciidoc"


@dataclass
class StyleViolation:
    rule_id: str
    line: int
    column: int
    message: str
    severity: Severity
    suggestion: Optional[str] = None
    context: str = ""


@dataclass
class ValidationResults:
    file_path: str
    violations: list[StyleViolation] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.WARNING)

    @property
    def passed(self) -> bool:
        return self.error_count == 0


@dataclass
class StyleRule:
    id: str
    name: str
    pattern: Optional[str] = None
    severity: Severity = Severity.WARNING
    suggestion: Optional[str] = None
    applies_to: list[str] = field(default_factory=list)
    terms: list[str] = field(default_factory=list)
    replacement_map: dict[str, str] = field(default_factory=dict)
    custom_checker: Optional[object] = None

    def matches_content_type(self, content_type: str) -> bool:
        if not self.applies_to:
            return True
        return content_type in self.applies_to


class StyleGuide:
    def __init__(self, project: str, rules: list[StyleRule]) -> None:
        self.project = project
        self.rules = rules
        self._compiled_patterns: dict[str, re.Pattern] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        for rule in self.rules:
            if rule.pattern:
                try:
                    self._compiled_patterns[rule.id] = re.compile(rule.pattern, re.IGNORECASE)
                except re.error as e:
                    raise ValueError(f"Invalid regex pattern in rule {rule.id}: {e}")

    def validate(self, file_path: str, content_type: str = "general") -> ValidationResults:
        results = ValidationResults(file_path=file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            results.violations.append(
                StyleViolation(rule_id="SYS-000", line=0, column=0,
                               message=f"File not found: {file_path}", severity=Severity.ERROR)
            )
            return results

        for rule in self.rules:
            if not rule.matches_content_type(content_type):
                continue
            if rule.pattern and rule.id in self._compiled_patterns:
                compiled = self._compiled_patterns[rule.id]
                for line_num, line in enumerate(lines, 1):
                    match = compiled.search(line)
                    if match:
                        results.violations.append(
                            StyleViolation(
                                rule_id=rule.id, line=line_num,
                                column=match.start(), message=rule.name,
                                severity=rule.severity, suggestion=rule.suggestion,
                                context=line.strip()
                            )
                        )
            if rule.terms:
                for line_num, line in enumerate(lines, 1):
                    for term in rule.terms:
                        if re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE):
                            replacement = rule.replacement_map.get(term.lower(), "")
                            suggestion = f"Replace '{term}' with '{replacement}'" if replacement else None
                            results.violations.append(
                                StyleViolation(
                                    rule_id=rule.id, line=line_num,
                                    column=0, message=f"Prohibited term: {term}",
                                    severity=rule.severity, suggestion=suggestion,
                                    context=line.strip()
                                )
                            )
        return results

    def auto_fix(self, file_path: str, dry_run: bool = True) -> list[StyleViolation]:
        fixable = []
        for rule in self.rules:
            if rule.replacement_map:
                fixable.append(
                    StyleViolation(rule_id=rule.id, line=0, column=0,
                                   message=f"Auto-fixable: {rule.name}",
                                   severity=rule.severity)
                )
        if not dry_run:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                for rule in self.rules:
                    for term, replacement in rule.replacement_map.items():
                        content = re.sub(rf"\b{re.escape(term)}\b", replacement, content, flags=re.IGNORECASE)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except FileNotFoundError:
                pass
        return fixable


@dataclass
class LinkEntry:
    source_file: str
    target: str
    line: int
    is_internal: bool = True
    exists: bool = True
    reason: str = ""


@dataclass
class LinkInventory:
    files: list[str] = field(default_factory=list)
    internal_links: list[LinkEntry] = field(default_factory=list)
    external_links: list[LinkEntry] = field(default_factory=list)
    anchors: dict[str, list[str]] = field(default_factory=dict)


class CrossReferenceManager:
    LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    ANCHOR_PATTERN = re.compile(r"^#+\s+(.+)$", re.MULTILINE)

    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)
        self.rename_map: dict[str, str] = {}
        self._inventory: Optional[LinkInventory] = None

    def build_inventory(self) -> LinkInventory:
        inventory = LinkInventory()
        md_files = list(self.root_dir.rglob("*.md"))
        inventory.files = [str(f.relative_to(self.root_dir)) for f in md_files]
        for md_file in md_files:
            rel_path = str(md_file.relative_to(self.root_dir))
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except FileNotFoundError:
                continue
            headers = self.ANCHOR_PATTERN.findall(content)
            inventory.anchors[rel_path] = [self._slugify(h) for h in headers]
            for line_num, line in enumerate(content.splitlines(), 1):
                for match in self.LINK_PATTERN.finditer(line):
                    target = match.group(2)
                    if target.startswith("#"):
                        anchor = target[1:]
                        exists = anchor in inventory.anchors.get(rel_path, [])
                        entry = LinkEntry(source_file=rel_path, target=target,
                                          line=line_num, is_internal=True,
                                          exists=exists,
                                          reason="" if exists else f"Anchor '{anchor}' not found")
                        inventory.internal_links.append(entry)
                    elif target.startswith(("http://", "https://")):
                        entry = LinkEntry(source_file=rel_path, target=target,
                                          line=line_num, is_internal=False, exists=True)
                        inventory.external_links.append(entry)
                    else:
                        target_path = md_file.parent / target
                        exists = target_path.exists()
                        entry = LinkEntry(source_file=rel_path, target=target,
                                          line=line_num, is_internal=True,
                                          exists=exists,
                                          reason="" if exists else f"File not found: {target}")
                        inventory.internal_links.append(entry)
        self._inventory = inventory
        return inventory

    def check_integrity(self) -> list[LinkEntry]:
        if self._inventory is None:
            self.build_inventory()
        assert self._inventory is not None
        return [link for link in self._inventory.internal_links if not link.exists]

    def _slugify(self, text: str) -> str:
        slug = text.lower().strip()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        return slug

    def update_references(self, dry_run: bool = True) -> list[tuple[str, str, str]]:
        updates = []
        for old_path, new_path in self.rename_map.items():
            old_rel = str(Path(old_path).relative_to(self.root_dir) if self.root_dir in Path(old_path).parents else Path(old_path))
            for md_file in self.root_dir.rglob("*.md"):
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                except FileNotFoundError:
                    continue
                new_content = content.replace(old_rel, new_path)
                if new_content != content:
                    updates.append((str(md_file), old_rel, new_path))
                    if not dry_run:
                        with open(md_file, "w", encoding="utf-8") as f:
                            f.write(new_content)
        return updates


@dataclass
class PDFOptions:
    page_size: str = "A4"
    margin: str = "2cm"
    toc_depth: int = 3
    header: str = ""
    footer: str = ""


@dataclass
class RenderResult:
    source: str
    output_format: OutputFormat
    output_path: str
    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class DocumentationRenderer:
    def __init__(self, template_dir: str = "", css_path: str = "",
                 base_url: str = "") -> None:
        self.template_dir = Path(template_dir) if template_dir else None
        self.css_path = css_path
        self.base_url = base_url
        self._templates: dict[str, str] = {}

    def render(self, source: str, output_format: OutputFormat,
               output_dir: str, pdf_options: Optional[dict] = None) -> list[RenderResult]:
        source_path = Path(source)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        results = []
        md_files = list(source_path.rglob("*.md"))
        for md_file in md_files:
            rel = md_file.relative_to(source_path)
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except FileNotFoundError as e:
                results.append(RenderResult(
                    source=str(md_file), output_format=output_format,
                    output_path="", success=False, errors=[str(e)]
                ))
                continue
            if output_format == OutputFormat.HTML:
                html_content = self._markdown_to_html(content)
                out_file = output_path / rel.with_suffix(".html")
                out_file.parent.mkdir(parents=True, exist_ok=True)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                results.append(RenderResult(
                    source=str(md_file), output_format=output_format,
                    output_path=str(out_file), success=True
                ))
            elif output_format == OutputFormat.PDF:
                out_file = output_path / rel.with_suffix(".pdf")
                out_file.parent.mkdir(parents=True, exist_ok=True)
                results.append(RenderResult(
                    source=str(md_file), output_format=output_format,
                    output_path=str(out_file), success=True,
                    warnings=["PDF rendering requires external toolchain"]
                ))
            elif output_format == OutputFormat.ASCIIDOC:
                adoc_content = self._markdown_to_asciidoc(content)
                out_file = output_path / rel.with_suffix(".adoc")
                out_file.parent.mkdir(parents=True, exist_ok=True)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(adoc_content)
                results.append(RenderResult(
                    source=str(md_file), output_format=output_format,
                    output_path=str(out_file), success=True
                ))
        return results

    def _markdown_to_html(self, content: str) -> str:
        html = content
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
        html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        return html

    def _markdown_to_asciidoc(self, content: str) -> str:
        adoc = content
        adoc = re.sub(r"^### (.+)$", r"==== \1", adoc, flags=re.MULTILINE)
        adoc = re.sub(r"^## (.+)$", r"=== \1", adoc, flags=re.MULTILINE)
        adoc = re.sub(r"^# (.+)$", r"== \1", adoc, flags=re.MULTILINE)
        adoc = re.sub(r"\*\*([^*]+)\*\*", r"*\1*", adoc)
        adoc = re.sub(r"`([^`]+)`", r"`\1`", adoc)
        return adoc


@dataclass
class DocumentMetadata:
    path: str
    title: str = ""
    author: str = ""
    last_updated: str = ""
    content_type: str = "general"
    word_count: int = 0
    heading_count: int = 0
    has_frontmatter: bool = False
    freshness_days: int = 0
    is_stale: bool = False


@dataclass
class FreshnessPolicy:
    content_type: str
    max_age_days: int = 365
    require_reviewer: bool = False
    notify_authors: bool = False


@dataclass
class AuditResult:
    total: int = 0
    stale_count: int = 0
    needs_review_count: int = 0
    stale_documents: list[DocumentMetadata] = field(default_factory=list)
    all_documents: list[DocumentMetadata] = field(default_factory=list)


class ContentLifecycleManager:
    def __init__(self, policies: list[FreshnessPolicy] | None = None) -> None:
        self.policies = {p.content_type: p for p in (policies or [])}
        self.default_policy = FreshnessPolicy(content_type="general", max_age_days=365)

    def audit(self, root_dir: str) -> AuditResult:
        result = AuditResult()
        root = Path(root_dir)
        now = datetime.datetime.now()
        for md_file in root.rglob("*.md"):
            meta = self._extract_metadata(md_file, now)
            result.all_documents.append(meta)
            result.total += 1
            policy = self.policies.get(meta.content_type, self.default_policy)
            if meta.freshness_days > policy.max_age_days:
                meta.is_stale = True
                result.stale_count += 1
                result.stale_documents.append(meta)
            if policy.require_reviewer:
                result.needs_review_count += 1
        return result

    def _extract_metadata(self, file_path: Path, now: datetime.datetime) -> DocumentMetadata:
        stat = file_path.stat()
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        freshness = (now - mtime).days
        word_count = 0
        heading_count = 0
        title = ""
        has_frontmatter = False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            words = content.split()
            word_count = len(words)
            heading_count = len(re.findall(r"^#+\s", content, re.MULTILINE))
            lines = content.splitlines()
            if lines and lines[0].strip() == "---":
                has_frontmatter = True
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
            if not title:
                for line in lines:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
        except (FileNotFoundError, UnicodeDecodeError):
            pass
        content_type = "general"
        rel_path = str(file_path)
        if "api" in rel_path.lower():
            content_type = "api-reference"
        elif "tutorial" in rel_path.lower():
            content_type = "tutorial"
        elif "architect" in rel_path.lower():
            content_type = "conceptual"
        elif "changelog" in rel_path.lower():
            content_type = "changelog"
        return DocumentMetadata(
            path=str(file_path), title=title, last_updated=mtime.isoformat(),
            content_type=content_type, word_count=word_count,
            heading_count=heading_count, has_frontmatter=has_frontmatter,
            freshness_days=freshness
        )

    def generate_report(self, audit: AuditResult, output: str = "audit-report.md") -> str:
        lines = [
            "# Documentation Audit Report\n",
            f"**Generated**: {datetime.datetime.now().isoformat()}\n",
            f"**Total Documents**: {audit.total}\n",
            f"**Stale Documents**: {audit.stale_count}\n",
            f"**Needs Review**: {audit.needs_review_count}\n",
            "\n## Stale Documents\n",
        ]
        for doc in audit.stale_documents:
            lines.append(f"- **{doc.title or doc.path}** — {doc.freshness_days} days old, last updated {doc.last_updated}")
        report = "\n".join(lines)
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(report)
        except OSError:
            pass
        return report


@dataclass
class GlossaryEntry:
    term: str
    definition: str
    aliases: list[str] = field(default_factory=list)
    category: str = "general"
    context: str = ""


class TerminologyManager:
    def __init__(self) -> None:
        self.entries: dict[str, GlossaryEntry] = {}
        self._usage_counts: dict[str, int] = {}

    def add_entry(self, entry: GlossaryEntry) -> None:
        key = entry.term.lower()
        self.entries[key] = entry
        for alias in entry.aliases:
            self.entries[alias.lower()] = entry

    def validate_file(self, file_path: str) -> list[tuple[int, str, str]]:
        violations = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return violations
        for line_num, line in enumerate(lines, 1):
            for entry in self.entries.values():
                if entry.aliases:
                    for alias in entry.aliases:
                        if re.search(rf"\b{re.escape(alias)}\b", line, re.IGNORECASE):
                            violations.append((line_num, alias, f"Use '{entry.term}' instead of '{alias}'"))
        return violations

    def generate_glossary(self, output_path: str = "glossary.md") -> str:
        lines = ["# Glossary\n"]
        by_category: dict[str, list[GlossaryEntry]] = {}
        seen = set()
        for entry in self.entries.values():
            if entry.term.lower() not in seen:
                seen.add(entry.term.lower())
                by_category.setdefault(entry.category, []).append(entry)
        for category, entries in sorted(by_category.items()):
            lines.append(f"\n## {category.title()}\n")
            for entry in sorted(entries, key=lambda e: e.term.lower()):
                lines.append(f"**{entry.term}**: {entry.definition}")
                if entry.aliases:
                    lines.append(f"  - Aliases: {', '.join(entry.aliases)}")
                lines.append("")
        report = "\n".join(lines)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
        except OSError:
            pass
        return report


@dataclass
class ReadabilityMetrics:
    file_path: str
    word_count: int
    sentence_count: int
    avg_words_per_sentence: float
    reading_level: str
    heading_hierarchy_valid: bool


class ContentQualityAnalyzer:
    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    SENTENCE_PATTERN = re.compile(r"[.!?]+\s+")

    def analyze(self, file_path: str) -> Optional[ReadabilityMetrics]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return None
        words = content.split()
        word_count = len(words)
        sentences = self.SENTENCE_PATTERN.split(content)
        sentence_count = max(len(sentences), 1)
        avg_words = word_count / sentence_count
        if avg_words < 15:
            level = "Easy"
        elif avg_words < 25:
            level = "Moderate"
        else:
            level = "Complex"
        headings = self.HEADING_PATTERN.findall(content)
        hierarchy_valid = True
        prev_level = 0
        for markers, _ in headings:
            current_level = len(markers)
            if current_level > prev_level + 1 and prev_level > 0:
                hierarchy_valid = False
                break
            prev_level = current_level
        return ReadabilityMetrics(
            file_path=file_path, word_count=word_count,
            sentence_count=sentence_count, avg_words_per_sentence=avg_words,
            reading_level=level, heading_hierarchy_valid=hierarchy_valid
        )


def main() -> None:
    print("=" * 60)
    print("Technical Documentation Authoring & Lifecycle Management")
    print("=" * 60)

    guide = StyleGuide(
        project="demo-project",
        rules=[
            StyleRule(id="SG-001", name="active-voice",
                      pattern=r"\b(is|are|was|were)\s+\w+ed\b",
                      severity=Severity.WARNING,
                      suggestion="Use active voice."),
            StyleRule(id="SG-002", name="no-jargon",
                      terms=["utilize", "leverage"],
                      replacement_map={"utilize": "use", "leverge": "use"},
                      severity=Severity.ERROR),
        ]
    )
    print("\n[StyleGuide] Rules loaded:", len(guide.rules))

    manager = CrossReferenceManager(root_dir="docs/")
    print("\n[CrossRef] Manager initialized for docs/")

    renderer = DocumentationRenderer(base_url="https://docs.example.com")
    print("\n[Renderer] Initialized with template support")

    lifecycle = ContentLifecycleManager(
        policies=[
            FreshnessPolicy(content_type="api-reference", max_age_days=90),
            FreshnessPolicy(content_type="tutorial", max_age_days=180),
        ]
    )
    print("\n[Lifecycle] Policies configured:", len(lifecycle.policies))

    glossary = TerminologyManager()
    glossary.add_entry(GlossaryEntry(
        term="API", definition="Application Programming Interface",
        aliases=["api", "Api"], category="technology"
    ))
    glossary.add_entry(GlossaryEntry(
        term="SDK", definition="Software Development Kit",
        aliases=["sdk", "Sdk"], category="technology"
    ))
    print("\n[Glossary] Entries loaded:", len(set(id(e) for e in glossary.entries.values())))

    analyzer = ContentQualityAnalyzer()
    print("\n[Quality] Analyzer ready")

    print("\n" + "=" * 60)
    print("All components initialized successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()

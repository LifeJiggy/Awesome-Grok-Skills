"""
Multi-Language Module
Multi-language content management and translation workflows
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ContentType(Enum):
    HTML = "html"
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"

class WorkflowStageType(Enum):
    MACHINE_TRANSLATE = "machine_translate"
    HUMAN_TRANSLATE = "human_translate"
    HUMAN_REVIEW = "human_review"
    APPROVAL = "approval"
    PUBLICATION = "publication"

class JobStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"

class TranslationProvider(Enum):
    DEEPL = "deepl"
    GOOGLE = "google"
    AWS = "aws"
    AZURE = "azure"

@dataclass
class ContentItem:
    content_id: str = ""
    content_type: ContentType = ContentType.HTML
    source_locale: str = "en-US"
    source_content: str = ""
    translations: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_translation(self, locale: str, content: str) -> None:
        self.translations[locale] = content
        self.updated_at = datetime.utcnow()

    def get_translation(self, locale: str) -> Optional[str]:
        return self.translations.get(locale)

@dataclass
class WorkflowStage:
    name: str = ""
    type: WorkflowStageType = WorkflowStageType.HUMAN_TRANSLATE
    provider: Optional[str] = None
    reviewer_pool: Optional[str] = None
    approver: Optional[str] = None

@dataclass
class TranslationJob:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    content_id: str = ""
    target_locales: List[str] = field(default_factory=list)
    status: JobStatus = JobStatus.PENDING
    priority: str = "normal"
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    progress: float = 0.0

@dataclass
class GlossaryTerm:
    term: str = ""
    translations: Dict[str, str] = field(default_factory=dict)
    domain: str = ""
    forbidden_terms: List[str] = field(default_factory=list)

@dataclass
class TranslationMemoryEntry:
    source: str = ""
    target: str = ""
    locale: str = ""
    context: str = ""
    quality_score: float = 1.0

class ContentManager:
    def __init__(self) -> None:
        self._content: Dict[str, ContentItem] = {}

    def add_content(self, item: ContentItem) -> None:
        self._content[item.content_id] = item

    def get_content(self, content_id: str, locale: str) -> Optional[str]:
        item = self._content.get(content_id)
        if item is None:
            return None
        return item.get_translation(locale) or item.source_content

    def list_content(self) -> List[ContentItem]:
        return list(self._content.values())

class TranslationWorkflow:
    def __init__(self, name: str = "", stages: Optional[List[WorkflowStage]] = None) -> None:
        self.name = name
        self.stages = stages or []
        self._jobs: List[TranslationJob] = []

    def submit(self, content_id: str, target_locales: List[str], priority: str = "normal") -> TranslationJob:
        job = TranslationJob(content_id=content_id, target_locales=target_locales, priority=priority)
        self._jobs.append(job)
        return job

    def get_jobs(self) -> List[TranslationJob]:
        return self._jobs

class GlossaryManager:
    def __init__(self) -> None:
        self._terms: Dict[str, GlossaryTerm] = {}

    def add_term(self, term: str, translations: Dict[str, str], domain: str = "", forbidden_terms: Optional[List[str]] = None) -> None:
        self._terms[term] = GlossaryTerm(term=term, translations=translations, domain=domain, forbidden_terms=forbidden_terms or [])

    def validate(self, text: str, target_locale: str) -> List[str]:
        violations = []
        text_lower = text.lower()
        for term, glossary_term in self._terms.items():
            for forbidden in glossary_term.forbidden_terms:
                if forbidden.lower() in text_lower:
                    violations.append(f"Found forbidden term '{forbidden}' (should use '{term}')")
        return violations

class TranslationMemory:
    def __init__(self) -> None:
        self._entries: List[TranslationMemoryEntry] = []

    def add_entry(self, source: str, target: str, locale: str, context: str = "") -> None:
        self._entries.append(TranslationMemoryEntry(source=source, target=target, locale=locale, context=context))

    def search(self, source: str, locale: str, threshold: float = 0.8) -> List[TranslationMemoryEntry]:
        results = []
        for entry in self._entries:
            if entry.locale == locale:
                similarity = self._calculate_similarity(source, entry.source)
                if similarity >= threshold:
                    results.append(entry)
        return sorted(results, key=lambda e: e.quality_score, reverse=True)

    def _calculate_similarity(self, a: str, b: str) -> float:
        if a == b:
            return 1.0
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())
        if not a_words or not b_words:
            return 0.0
        intersection = a_words & b_words
        return len(intersection) / max(len(a_words), len(b_words))

class CoverageDashboard:
    def __init__(self, content_manager: ContentManager) -> None:
        self._manager = content_manager

    def get_coverage(self, locale: str) -> Dict[str, Any]:
        items = self._manager.list_content()
        total = len(items)
        translated = sum(1 for item in items if item.get_translation(locale))
        return {"total_items": total, "translated": translated, "coverage_pct": (translated / total * 100) if total > 0 else 0, "outdated": 0}

def main() -> None:
    print("=" * 60)
    print("  Multi-Language Module — Demo")
    print("=" * 60)

    manager = ContentManager()
    item = ContentItem(content_id="home-hero", source_content="<h1>Welcome</h1>")
    item.add_translation("es-ES", "<h1>Bienvenido</h1>")
    manager.add_content(item)
    print(f"\n[+] Content: {manager.get_content('home-hero', 'es-ES')}")

    workflow = TranslationWorkflow(name="product-descriptions")
    job = workflow.submit("product-123", ["es-ES", "fr-FR"])
    print(f"[+] Job: {job.job_id} ({job.status.value})")

    glossary = GlossaryManager()
    glossary.add_term("cloud computing", {"es-ES": "nube"}, forbidden_terms=["cloud"])
    violations = glossary.validate("Computing in the cloud", "es-ES")
    print(f"[+] Glossary violations: {violations}")

    tm = TranslationMemory()
    tm.add_entry("Welcome to our platform", "Bienvenido a nuestra plataforma", "es-ES")
    matches = tm.search("Welcome to our platform today", "es-ES")
    print(f"[+] TM matches: {len(matches)}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

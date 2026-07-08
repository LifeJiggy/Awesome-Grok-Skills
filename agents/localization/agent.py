"""
Localization Agent - Internationalization, Translation Workflows, and Cultural Adaptation.

Comprehensive localization platform covering translation memory management,
i18n/l10n engineering, cultural adaptation, quality assurance, terminology
management, and multi-market deployment. Built for product teams shipping
software across languages and regions, managing large-scale translation
projects with consistency, quality, and efficiency.

Key Capabilities:
- Translation Memory: Deduplication, leverage, fuzzy matching, TM maintenance
- i18n Engineering: Pseudo-localization, resource file management, RTL support
- Cultural Adaptation: Locale-aware formatting, content adaptation, cultural QA
- Quality Assurance: Linguistic QA, automated checks, style guide enforcement
- Terminology Management: Glossaries, termbases, consistency enforcement
- Project Management: Workflow orchestration, vendor coordination, deadline tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import uuid
import re
import math
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_TRADITIONAL = "zh-TW"
    JAPANESE = "ja"
    KOREAN = "ko"
    PORTUGUESE_BR = "pt-BR"
    PORTUGUESE_PT = "pt-PT"
    ITALIAN = "it"
    RUSSIAN = "ru"
    ARABIC = "ar"
    HINDI = "hi"
    TURKISH = "tr"
    DUTCH = "nl"
    SWEDISH = "sv"
    POLISH = "pl"
    THAI = "th"
    VIETNAMESE = "vi"


class TextDirection(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TranslationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    TRANSLATED = "translated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"
    OUTDATED = "outdated"
    DEPRECATED = "deprecated"


class QASeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class QACheckType(Enum):
    MISSING_TRANSLATION = "missing_translation"
    PLACEHOLDER_MISMATCH = "placeholder_mismatch"
    LENGTH_ISSUE = "length_issue"
    ENCODING_ERROR = "encoding_error"
    FORMATTING_ERROR = "formatting_error"
    GLOSSARY_VIOLATION = "glossary_violation"
    STYLE_VIOLATION = "style_violation"
    CULTURAL_ISSUE = "cultural_issue"
    NUMERIC_FORMAT = "numeric_format"
    DATE_FORMAT = "date_format"
    PLURAL_FORM = "plural_form"
    CONTEXT_MISMATCH = "context_mismatch"
    PUNCTUATION = "punctuation"
    TERMINOLOGY = "terminology"
    BRAND_VOICE = "brand_voice"


class ProjectPhase(Enum):
    PLANNING = "planning"
    EXTRACTION = "extraction"
    TRANSLATION = "translation"
    REVIEW = "review"
    QA = "qa"
    INTEGRATION = "integration"
    LAUNCH = "launch"
    POST_LAUNCH = "post_launch"


class MatchType(Enum):
    EXACT = "exact"
    FUZZY_95 = "fuzzy_95"
    FUZZY_85 = "fuzzy_85"
    FUZZY_75 = "fuzzy_75"
    MT = "machine_translation"
    NEW = "new"


class WorkflowStep(Enum):
    EXTRACT = "extract"
    TRANSLATE = "translate"
    REVIEW = "review"
    PROOFREAD = "proofread"
    QA_CHECK = "qa_check"
    INTEGRATE = "integrate"
    PUBLISH = "publish"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TranslationUnit:
    """A single translatable string."""
    unit_id: str
    key: str
    source_text: str
    source_language: str
    target_language: str
    translated_text: str = ""
    status: TranslationStatus = TranslationStatus.PENDING
    context: str = ""
    character_limit: int = 0
    plural_forms: Dict[str, str] = field(default_factory=dict)
    notes: str = ""
    translator: str = ""
    reviewer: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    match_type: MatchType = MatchType.NEW
    match_source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationMemoryEntry:
    """A translation memory entry."""
    entry_id: str
    source_text: str
    target_text: str
    source_language: str
    target_language: str
    domain: str = ""
    created_by: str = ""
    usage_count: int = 0
    approved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class TerminologyEntry:
    """A terminology/glossary entry."""
    term_id: str
    source_term: str
    target_term: str
    source_language: str
    target_language: str
    definition: str = ""
    part_of_speech: str = ""
    context: str = ""
    do_not_translate: bool = False
    forbidden_alternatives: List[str] = field(default_factory=list)
    domain: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class QAIssue:
    """A quality assurance issue."""
    issue_id: str
    unit_id: str
    check_type: QACheckType
    severity: QASeverity
    message: str
    language: str = ""
    suggestion: str = ""
    auto_fixable: bool = False
    resolved: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class LocalizationProject:
    """A localization project."""
    project_id: str
    name: str
    source_language: str
    target_languages: List[str]
    status: str = "active"
    phase: ProjectPhase = ProjectPhase.PLANNING
    total_strings: int = 0
    translated_count: int = 0
    reviewed_count: int = 0
    approved_count: int = 0
    team: List[str] = field(default_factory=list)
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    workflow_steps: List[WorkflowStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LocaleConfig:
    """Locale-specific configuration."""
    locale: str
    language: str
    region: str
    direction: TextDirection = TextDirection.LTR
    date_format: str = "YYYY-MM-DD"
    time_format: str = "HH:mm"
    number_format: str = "1,234.56"
    currency_code: str = "USD"
    currency_symbol: str = "$"
    decimal_separator: str = "."
    thousands_separator: str = ","
    first_day_of_week: int = 1
    plural_rules: str = "english"
    collation: str = "default"
    character_set: str = "utf-8"


@dataclass
class StyleGuide:
    """A style guide for a target language."""
    guide_id: str
    language: str
    rules: List[Dict[str, str]] = field(default_factory=list)
    tone: str = ""
    formality: str = ""
    brand_voices: Dict[str, str] = field(default_factory=dict)
    examples: List[Dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Translation Memory Engine
# ---------------------------------------------------------------------------

class TranslationMemoryEngine:
    """Manages translation memory for deduplication and leverage."""

    def __init__(self, fuzzy_threshold: float = 0.75) -> None:
        self.entries: Dict[str, TranslationMemoryEntry] = {}
        self.fuzzy_threshold = fuzzy_threshold

    def add_entry(self, source_text: str, target_text: str,
                  source_lang: str, target_lang: str,
                  domain: str = "", approved: bool = True) -> TranslationMemoryEntry:
        entry_id = f"TM-{hashlib.md5(source_text.encode()).hexdigest()[:8].upper()}"
        entry = TranslationMemoryEntry(
            entry_id=entry_id,
            source_text=source_text,
            target_text=target_text,
            source_language=source_lang,
            target_language=target_lang,
            domain=domain,
            approved=approved,
        )
        self.entries[entry_id] = entry
        return entry

    def fuzzy_match_score(self, text_a: str, text_b: str) -> float:
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())
        if not words_a or not words_b:
            return 0.0
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union) if union else 0.0

    def find_matches(self, source_text: str, source_lang: str,
                     target_lang: str, limit: int = 5) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for entry in self.entries.values():
            if entry.source_language != source_lang or entry.target_language != target_lang:
                continue
            score = self.fuzzy_match_score(source_text, entry.source_text)
            if score >= self.fuzzy_threshold:
                match_type = MatchType.EXACT if score >= 1.0 else (
                    MatchType.FUZZY_95 if score >= 0.95 else (
                        MatchType.FUZZY_85 if score >= 0.85 else MatchType.FUZZY_75
                    )
                )
                matches.append({
                    "entry_id": entry.entry_id,
                    "source": entry.source_text,
                    "target": entry.target_text,
                    "score": round(score, 3),
                    "match_type": match_type.value,
                    "approved": entry.approved,
                })
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:limit]

    def get_leverage_stats(self, source_lang: str, target_lang: str,
                           source_texts: List[str]) -> Dict[str, Any]:
        exact = 0
        fuzzy = 0
        new = 0
        for text in source_texts:
            matches = self.find_matches(text, source_lang, target_lang, limit=1)
            if matches:
                if matches[0]["match_type"] == "exact":
                    exact += 1
                else:
                    fuzzy += 1
            else:
                new += 1
        total = len(source_texts)
        return {
            "total_strings": total,
            "exact_matches": exact,
            "fuzzy_matches": fuzzy,
            "new_strings": new,
            "leverage_percent": round((exact + fuzzy * 0.75) / max(1, total) * 100, 1),
            "cost_savings_estimate": f"{round((exact + fuzzy * 0.75) / max(1, total) * 100, 0)}%",
        }

    def maintenance_report(self) -> Dict[str, Any]:
        by_lang: Dict[str, int] = defaultdict(int)
        by_domain: Dict[str, int] = defaultdict(int)
        approved = 0
        for entry in self.entries.values():
            by_lang[f"{entry.source_language}-{entry.target_language}"] += 1
            by_domain[entry.domain or "general"] += 1
            if entry.approved:
                approved += 1
        return {
            "total_entries": len(self.entries),
            "approved_entries": approved,
            "pending_review": len(self.entries) - approved,
            "by_language_pair": dict(by_lang),
            "by_domain": dict(by_domain),
            "utilization_rate": round(
                sum(e.usage_count for e in self.entries.values()) / max(1, len(self.entries)), 1
            ),
        }


# ---------------------------------------------------------------------------
# i18n Engine
# ---------------------------------------------------------------------------

class I18nEngine:
    """Handles internationalization engineering tasks."""

    def __init__(self) -> None:
        self.locale_configs: Dict[str, LocaleConfig] = {}
        self.resource_files: Dict[str, Dict[str, str]] = {}
        self.pseudo_localizations: Dict[str, str] = {}

    def register_locale(self, locale: str, language: str, region: str,
                        **kwargs: Any) -> LocaleConfig:
        direction = TextDirection.RTL if language in ("ar", "he", "fa", "ur") else TextDirection.LTR
        config = LocaleConfig(
            locale=locale,
            language=language,
            region=region,
            direction=direction,
            date_format=kwargs.get("date_format", "YYYY-MM-DD"),
            time_format=kwargs.get("time_format", "HH:mm"),
            number_format=kwargs.get("number_format", "1,234.56"),
            currency_code=kwargs.get("currency", "USD"),
            currency_symbol=kwargs.get("currency_symbol", "$"),
            decimal_separator=kwargs.get("decimal_sep", "."),
            thousands_separator=kwargs.get("thousands_sep", ","),
            plural_rules=kwargs.get("plural_rules", "english"),
        )
        self.locale_configs[locale] = config
        return config

    def generate_pseudo_localization(self, source_strings: Dict[str, str],
                                      target_locale: str) -> Dict[str, str]:
        config = self.locale_configs.get(target_locale)
        pseudo = {}
        prefix = "¡" if config and config.direction == TextDirection.LTR else ""
        suffix = "!" if config and config.direction == TextDirection.LTR else ""
        for key, text in source_strings.items():
            expanded = re.sub(r'[aeiou]', lambda m: m.group(0) * 2, text)
            pseudo[key] = f"{prefix}{expanded}{suffix}"
        self.pseudo_localizations[target_locale] = json.dumps(pseudo, ensure_ascii=False)
        return pseudo

    def format_number(self, value: float, locale: str) -> str:
        config = self.locale_configs.get(locale)
        if not config:
            return str(value)
        formatted = f"{value:,.2f}"
        formatted = formatted.replace(",", "TEMP").replace(".", config.decimal_separator)
        formatted = formatted.replace("TEMP", config.thousands_separator)
        return formatted

    def format_date(self, dt: datetime, locale: str) -> str:
        config = self.locale_configs.get(locale)
        if not config:
            return dt.strftime("%Y-%m-%d")
        fmt = config.date_format
        fmt = fmt.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
        try:
            return dt.strftime(fmt)
        except ValueError:
            return dt.strftime("%Y-%m-%d")

    def format_currency(self, value: float, locale: str) -> str:
        config = self.locale_configs.get(locale)
        if not config:
            return f"${value:,.2f}"
        formatted = self.format_number(value, locale)
        if config.direction == TextDirection.RTL:
            return f"{formatted} {config.currency_symbol}"
        return f"{config.currency_symbol}{formatted}"

    def check_rtl_support(self, locale: str) -> Dict[str, Any]:
        config = self.locale_configs.get(locale)
        if not config:
            return {"error": f"Locale {locale} not found"}
        return {
            "locale": locale,
            "direction": config.direction.value,
            "needs_rtl": config.direction == TextDirection.RTL,
            "css_recommendation": "dir='rtl' on <html> element",
            "layout_flipping": config.direction == TextDirection.RTL,
            "mirror_icons": config.direction == TextDirection.RTL,
        }

    def load_resource_file(self, locale: str, strings: Dict[str, str]) -> None:
        self.resource_files[locale] = strings

    def check_missing_keys(self, source_locale: str, target_locale: str) -> Dict[str, Any]:
        source = self.resource_files.get(source_locale, {})
        target = self.resource_files.get(target_locale, {})
        missing = [k for k in source if k not in target]
        extra = [k for k in target if k not in source]
        return {
            "source_locale": source_locale,
            "target_locale": target_locale,
            "source_keys": len(source),
            "target_keys": len(target),
            "missing_keys": missing,
            "extra_keys": extra,
            "completeness": round(len(target) / max(1, len(source)) * 100, 1),
        }


# ---------------------------------------------------------------------------
# Cultural Adaptation Engine
# ---------------------------------------------------------------------------

class CulturalAdaptationEngine:
    """Handles cultural adaptation and locale-aware content."""

    def __init__(self) -> None:
        self.style_guides: Dict[str, StyleGuide] = {}
        self.cultural_rules: Dict[str, List[Dict[str, Any]]] = {}

    def register_style_guide(self, language: str, tone: str, formality: str,
                              rules: Optional[List[Dict[str, str]]] = None) -> StyleGuide:
        guide_id = f"SG-{hashlib.md5(language.encode()).hexdigest()[:8].upper()}"
        guide = StyleGuide(
            guide_id=guide_id,
            language=language,
            tone=tone,
            formality=formality,
            rules=rules or [],
        )
        self.style_guides[language] = guide
        return guide

    def add_cultural_rule(self, language: str, rule_type: str,
                          description: str, examples: Optional[List[str]] = None) -> None:
        if language not in self.cultural_rules:
            self.cultural_rules[language] = []
        self.cultural_rules[language].append({
            "type": rule_type,
            "description": description,
            "examples": examples or [],
        })

    def adapt_content(self, text: str, source_locale: str,
                      target_locale: str) -> Dict[str, Any]:
        adaptations: List[str] = []
        source_config = self.locale_configs.get(source_locale) if hasattr(self, 'locale_configs') else None
        target_guide = self.style_guides.get(target_locale.split("-")[0])

        if target_guide:
            if target_guide.formality == "formal":
                adaptations.append("Apply formal register")
            elif target_guide.formality == "informal":
                adaptations.append("Apply casual tone")

        cultural = self.cultural_rules.get(target_locale.split("-")[0], [])
        for rule in cultural:
            adaptations.append(f"Cultural rule: {rule['description']}")

        return {
            "original": text,
            "source_locale": source_locale,
            "target_locale": target_locale,
            "adaptations_needed": adaptations,
            "style_guide_applied": target_guide is not None,
            "cultural_rules_checked": len(cultural),
        }

    def get_culture_report(self, language: str) -> Dict[str, Any]:
        guide = self.style_guides.get(language)
        rules = self.cultural_rules.get(language, [])
        return {
            "language": language,
            "has_style_guide": guide is not None,
            "tone": guide.tone if guide else "unknown",
            "formality": guide.formality if guide else "unknown",
            "rules_count": len(rules),
            "rule_types": list(set(r["type"] for r in rules)),
        }


# ---------------------------------------------------------------------------
# Quality Assurance Engine
# ---------------------------------------------------------------------------

class QualityAssuranceEngine:
    """Automated and manual quality assurance for translations."""

    def __init__(self) -> None:
        self.issues: List[QAIssue] = []
        self.check_results: Dict[str, Dict[str, Any]] = {}

    def check_missing_translations(self, units: List[TranslationUnit]) -> List[QAIssue]:
        issues: List[QAIssue] = []
        for unit in units:
            if not unit.translated_text:
                issue = QAIssue(
                    issue_id=f"QA-{uuid.uuid4().hex[:8]}",
                    unit_id=unit.unit_id,
                    check_type=QACheckType.MISSING_TRANSLATION,
                    severity=QASeverity.CRITICAL,
                    message=f"Missing translation for key '{unit.key}'",
                    language=unit.target_language,
                )
                issues.append(issue)
        self.issues.extend(issues)
        return issues

    def check_placeholder_consistency(self, units: List[TranslationUnit]) -> List[QAIssue]:
        issues: List[QAIssue] = []
        placeholder_pattern = re.compile(r'\{[^}]+\}|%[sd]|%\.\d+f|\$\w+')
        for unit in units:
            if not unit.translated_text:
                continue
            source_placeholders = set(placeholder_pattern.findall(unit.source_text))
            target_placeholders = set(placeholder_pattern.findall(unit.translated_text))
            missing = source_placeholders - target_placeholders
            extra = target_placeholders - source_placeholders
            if missing or extra:
                issues.append(QAIssue(
                    issue_id=f"QA-{uuid.uuid4().hex[:8]}",
                    unit_id=unit.unit_id,
                    check_type=QACheckType.PLACEHOLDER_MISMATCH,
                    severity=QASeverity.HIGH,
                    message=f"Placeholder mismatch: missing={missing}, extra={extra}",
                    language=unit.target_language,
                    suggestion=f"Ensure all placeholders {source_placeholders} are present",
                ))
        self.issues.extend(issues)
        return issues

    def check_length_limits(self, units: List[TranslationUnit],
                            max_ratio: float = 2.0) -> List[QAIssue]:
        issues: List[QAIssue] = []
        for unit in units:
            if not unit.translated_text or not unit.character_limit:
                continue
            if len(unit.translated_text) > unit.character_limit:
                issues.append(QAIssue(
                    issue_id=f"QA-{uuid.uuid4().hex[:8]}",
                    unit_id=unit.unit_id,
                    check_type=QACheckType.LENGTH_ISSUE,
                    severity=QASeverity.MEDIUM,
                    message=f"Translation ({len(unit.translated_text)} chars) exceeds limit ({unit.character_limit})",
                    language=unit.target_language,
                ))
            ratio = len(unit.translated_text) / max(1, len(unit.source_text))
            if ratio > max_ratio:
                issues.append(QAIssue(
                    issue_id=f"QA-{uuid.uuid4().hex[:8]}",
                    unit_id=unit.unit_id,
                    check_type=QACheckType.LENGTH_ISSUE,
                    severity=QASeverity.LOW,
                    message=f"Translation is {ratio:.1f}x the source length",
                    language=unit.target_language,
                ))
        self.issues.extend(issues)
        return issues

    def check_glossary_compliance(self, units: List[TranslationUnit],
                                   glossary: List[TerminologyEntry]) -> List[QAIssue]:
        issues: List[QAIssue] = []
        glossary_map: Dict[str, Dict[str, str]] = defaultdict(dict)
        for entry in glossary:
            glossary_map[entry.source_language][entry.source_term.lower()] = entry.target_term
        for unit in units:
            if not unit.translated_text:
                continue
            target_glossary = glossary_map.get(unit.target_language, {})
            for source_term, correct_term in target_glossary.items():
                if source_term in unit.source_text.lower():
                    if correct_term.lower() not in unit.translated_text.lower():
                        alternatives = [
                            e.forbidden_alternatives
                            for e in glossary
                            if e.source_term.lower() == source_term
                            and e.target_language == unit.target_language
                        ]
                        issues.append(QAIssue(
                            issue_id=f"QA-{uuid.uuid4().hex[:8]}",
                            unit_id=unit.unit_id,
                            check_type=QACheckType.GLOSSARY_VIOLATION,
                            severity=QASeverity.HIGH,
                            message=f"Term '{source_term}' should be translated as '{correct_term}'",
                            language=unit.target_language,
                            suggestion=f"Use '{correct_term}' instead",
                        ))
        self.issues.extend(issues)
        return issues

    def run_full_qa(self, units: List[TranslationUnit],
                    glossary: Optional[List[TerminologyEntry]] = None) -> Dict[str, Any]:
        all_issues: List[QAIssue] = []
        all_issues.extend(self.check_missing_translations(units))
        all_issues.extend(self.check_placeholder_consistency(units))
        all_issues.extend(self.check_length_limits(units))
        if glossary:
            all_issues.extend(self.check_glossary_compliance(units, glossary))

        by_severity: Dict[str, int] = defaultdict(int)
        by_type: Dict[str, int] = defaultdict(int)
        auto_fixable = 0
        for issue in all_issues:
            by_severity[issue.severity.value] += 1
            by_type[issue.check_type.value] += 1
            if issue.auto_fixable:
                auto_fixable += 1

        return {
            "total_issues": len(all_issues),
            "by_severity": dict(by_severity),
            "by_type": dict(by_type),
            "auto_fixable": auto_fixable,
            "manual_review_needed": len(all_issues) - auto_fixable,
            "pass_rate": round(
                max(0, 1 - len(all_issues) / max(1, len(units))) * 100, 1
            ),
        }

    def get_issue_summary(self) -> Dict[str, Any]:
        unresolved = [i for i in self.issues if not i.resolved]
        by_severity: Dict[str, int] = defaultdict(int)
        for issue in unresolved:
            by_severity[issue.severity.value] += 1
        return {
            "total_issues": len(self.issues),
            "unresolved": len(unresolved),
            "resolved": len(self.issues) - len(unresolved),
            "by_severity": dict(by_severity),
        }


# ---------------------------------------------------------------------------
# Localization Project Manager
# ---------------------------------------------------------------------------

class LocalizationProjectManager:
    """Manages localization projects and workflows."""

    def __init__(self) -> None:
        self.projects: Dict[str, LocalizationProject] = {}
        self.workflow_history: List[Dict[str, Any]] = []

    def create_project(self, name: str, source_language: str,
                       target_languages: List[str],
                       **kwargs: Any) -> LocalizationProject:
        project_id = f"L10N-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        project = LocalizationProject(
            project_id=project_id,
            name=name,
            source_language=source_language,
            target_languages=target_languages,
            total_strings=kwargs.get("total_strings", 0),
            team=kwargs.get("team", []),
            deadline=kwargs.get("deadline"),
            workflow_steps=kwargs.get("workflow", [
                WorkflowStep.EXTRACT,
                WorkflowStep.TRANSLATE,
                WorkflowStep.REVIEW,
                WorkflowStep.QA_CHECK,
                WorkflowStep.INTEGRATE,
                WorkflowStep.PUBLISH,
            ]),
        )
        self.projects[project_id] = project
        return project

    def advance_phase(self, project_id: str) -> Dict[str, Any]:
        project = self.projects.get(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}
        phases = list(ProjectPhase)
        idx = phases.index(project.phase)
        if idx < len(phases) - 1:
            project.phase = phases[idx + 1]
            project.updated_at = datetime.now()
            self.workflow_history.append({
                "project_id": project_id,
                "from_phase": phases[idx].value,
                "to_phase": project.phase.value,
                "timestamp": datetime.now().isoformat(),
            })
        return {
            "project_id": project_id,
            "new_phase": project.phase.value,
            "name": project.name,
        }

    def update_progress(self, project_id: str, language: str,
                        translated: int, reviewed: int,
                        approved: int) -> Dict[str, Any]:
        project = self.projects.get(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}
        project.translated_count += translated
        project.reviewed_count += reviewed
        project.approved_count += approved
        project.updated_at = datetime.now()
        overall = round(project.approved_count / max(1, project.total_strings) * 100, 1)
        return {
            "project_id": project_id,
            "language": language,
            "translated": translated,
            "reviewed": reviewed,
            "approved": approved,
            "overall_progress": overall,
        }

    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        project = self.projects.get(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}
        overall = round(project.approved_count / max(1, project.total_strings) * 100, 1)
        days_remaining = None
        if project.deadline:
            days_remaining = (project.deadline - datetime.now()).days
        return {
            "project_id": project_id,
            "name": project.name,
            "phase": project.phase.value,
            "source_language": project.source_language,
            "target_languages": project.target_languages,
            "total_strings": project.total_strings,
            "translated": project.translated_count,
            "reviewed": project.reviewed_count,
            "approved": project.approved_count,
            "overall_progress": overall,
            "days_remaining": days_remaining,
            "team_size": len(project.team),
        }

    def get_portfolio_overview(self) -> Dict[str, Any]:
        by_phase: Dict[str, int] = defaultdict(int)
        total_strings = 0
        total_approved = 0
        for project in self.projects.values():
            by_phase[project.phase.value] += 1
            total_strings += project.total_strings
            total_approved += project.approved_count
        return {
            "total_projects": len(self.projects),
            "by_phase": dict(by_phase),
            "total_strings": total_strings,
            "total_approved": total_approved,
            "overall_completion": round(total_approved / max(1, total_strings) * 100, 1),
        }


# ---------------------------------------------------------------------------
# Localization Agent (Orchestrator)
# ---------------------------------------------------------------------------

class LocalizationAgent:
    """Orchestrates all localization components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.tm_engine = TranslationMemoryEngine(fuzzy_threshold=config.get("fuzzy_threshold", 0.75))
        self.i18n_engine = I18nEngine()
        self.cultural_engine = CulturalAdaptationEngine()
        self.qa_engine = QualityAssuranceEngine()
        self.project_manager = LocalizationProjectManager()
        self._initialized_at = datetime.now()
        logger.info("LocalizationAgent initialized")

    def get_dashboard(self) -> Dict[str, Any]:
        return {
            "projects": self.project_manager.get_portfolio_overview(),
            "translation_memory": self.tm_engine.maintenance_report(),
            "qa_summary": self.qa_engine.get_issue_summary(),
            "locales_registered": len(self.i18n_engine.locale_configs),
            "style_guides": len(self.cultural_engine.style_guides),
            "uptime": str(datetime.now() - self._initialized_at),
        }


def _demo() -> None:
    agent = LocalizationAgent()

    # Add TM entries
    agent.tm_engine.add_entry("Hello World", "Hola Mundo", "en", "es", "greeting")
    agent.tm_engine.add_entry("Welcome back", "Bienvenido de nuevo", "en", "es", "greeting")
    matches = agent.tm_engine.find_matches("Hello World!", "en", "es")
    print(f"TM matches: {len(matches)}")

    # Register locales
    agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR", currency_symbol="\u20ac")
    agent.i18n_engine.register_locale("ar-SA", "ar", "SA")
    print(f"Number format: {agent.i18n_engine.format_number(1234.56, 'es-ES')}")
    print(f"Currency: {agent.i18n_engine.format_currency(99.99, 'es-ES')}")

    # Style guide
    agent.cultural_engine.register_style_guide("es", tone="warm", formality="formal")
    agent.cultural_engine.add_cultural_rule("es", "formality", "Use usted in B2B contexts")
    adaptation = agent.cultural_engine.adapt_content("Buy now", "en", "es-ES")
    print(f"Adaptations needed: {len(adaptation['adaptations_needed'])}")

    # QA
    units = [
        TranslationUnit(unit_id="U1", key="greeting", source_text="Hello {name}", target_language="es", translated_text="Hola {name}"),
        TranslationUnit(unit_id="U2", key="farewell", source_text="Goodbye", target_language="es", translated_text=""),
    ]
    qa_result = agent.qa_engine.run_full_qa(units)
    print(f"QA: {qa_result['total_issues']} issues, pass rate {qa_result['pass_rate']}%")

    # Project
    project = agent.project_manager.create_project(
        name="Product Launch ES",
        source_language="en",
        target_languages=["es", "fr", "de"],
        total_strings=5000,
    )
    agent.project_manager.advance_phase(project.project_id)
    agent.project_manager.update_progress(project.project_id, "es", translated=1000, reviewed=500, approved=400)
    status = agent.project_manager.get_project_status(project.project_id)
    print(f"Project progress: {status['overall_progress']}%")

    dashboard = agent.get_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2, default=str)}")


if __name__ == "__main__":
    _demo()

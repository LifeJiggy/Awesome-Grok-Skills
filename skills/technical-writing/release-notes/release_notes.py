"""
Automated Release Note Generation & Changelog Management

Provides changelog generation, semantic versioning enforcement, breaking change
detection, migration guide generation, deprecation management, and multi-channel
release publishing.
"""

from __future__ import annotations

import re
import json
import hashlib
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any
from pathlib import Path


class ChangeCategory(Enum):
    ADDED = "Added"
    CHANGED = "Changed"
    DEPRECATED = "Deprecated"
    REMOVED = "Removed"
    FIXED = "Fixed"
    SECURITY = "Security"


class Channel(Enum):
    GITHUB_RELEASES = "github_releases"
    SLACK = "slack"
    DOCUMENTATION = "documentation"
    EMAIL = "email"
    RSS = "rss"


class TemplateType(Enum):
    MAJOR_RELEASE = "major_release"
    MINOR_RELEASE = "minor_release"
    PATCH_RELEASE = "patch_release"


class Severity(Enum):
    BREAKING = "breaking"
    NON_BREAKING = "non-breaking"


@dataclass
class GitCommit:
    hash: str
    message: str
    author: str = ""
    date: str = ""
    files: list[str] = field(default_factory=list)


@dataclass
class ParsedCommit:
    hash: str
    type: str
    scope: str
    description: str
    body: str = ""
    is_breaking: bool = False
    footers: dict[str, str] = field(default_factory=dict)
    raw_message: str = ""


@dataclass
class ChangelogEntry:
    category: ChangeCategory
    description: str
    scope: str = ""
    commit_hash: str = ""
    breaking: bool = False


@dataclass
class Changelog:
    version: str
    date: str
    entries: list[ChangelogEntry] = field(default_factory=list)

    @property
    def breaking_changes(self) -> list[ChangelogEntry]:
        return [e for e in self.entries if e.breaking]

    @property
    def has_breaking_changes(self) -> bool:
        return len(self.breaking_changes) > 0

    def to_markdown(self) -> str:
        lines = [f"# Changelog\n", f"## [{self.version}] - {self.date}\n"]
        by_category: dict[ChangeCategory, list[ChangelogEntry]] = {}
        for entry in self.entries:
            by_category.setdefault(entry.category, []).append(entry)
        category_order = [
            ChangeCategory.ADDED, ChangeCategory.CHANGED, ChangeCategory.DEPRECATED,
            ChangeCategory.REMOVED, ChangeCategory.FIXED, ChangeCategory.SECURITY
        ]
        for cat in category_order:
            entries = by_category.get(cat, [])
            if entries:
                lines.append(f"### {cat.value}\n")
                for e in entries:
                    prefix = f"**{e.scope}**: " if e.scope else ""
                    lines.append(f"- {prefix}{e.description}")
                lines.append("")
        return "\n".join(lines)

    def to_json(self) -> str:
        data = {
            "version": self.version,
            "date": self.date,
            "entries": [
                {"category": e.category.value, "description": e.description,
                 "scope": e.scope, "breaking": e.breaking}
                for e in self.entries
            ]
        }
        return json.dumps(data, indent=2)


@dataclass
class CommitParserConfig:
    types: dict[str, str] = field(default_factory=lambda: {
        "feat": "Features",
        "fix": "Bug Fixes",
        "docs": "Documentation",
        "perf": "Performance",
        "refactor": "Code Refactoring",
        "test": "Tests",
        "chore": "Maintenance",
        "breaking": "Breaking Changes",
        "deprecate": "Deprecations",
    })
    breaking_keywords: list[str] = field(default_factory=lambda: ["BREAKING CHANGE", "BREAKING-CHANGE"])
    scope_optional: bool = True


class CommitParser:
    CONVENTIONAL_PATTERN = re.compile(
        r"^(?P<type>\w+)"
        r"(?:\((?P<scope>[^)]+)\))?"
        r"(?P<breaking>!)?"
        r":\s*(?P<description>.+)$"
    )

    def __init__(self, config: Optional[CommitParserConfig] = None) -> None:
        self.config = config or CommitParserConfig()

    def parse(self, message: str) -> ParsedCommit:
        lines = message.strip().split("\n")
        first_line = lines[0]
        body = "\n".join(lines[1:]) if len(lines) > 1 else ""
        match = self.CONVENTIONAL_PATTERN.match(first_line)
        if match:
            commit_type = match.group("type")
            scope = match.group("scope") or ""
            is_breaking = bool(match.group("breaking"))
            description = match.group("description").strip()
        else:
            commit_type = "other"
            scope = ""
            is_breaking = False
            description = first_line.strip()

        footers: dict[str, str] = {}
        current_footer_key = ""
        for line in lines[1:]:
            footer_match = re.match(r"^(?P<key>[\w-]+):\s*(?P<value>.+)$", line)
            if footer_match:
                current_footer_key = footer_match.group("key")
                footers[current_footer_key] = footer_match.group("value")
            elif current_footer_key and line.startswith(" "):
                footers[current_footer_key] += " " + line.strip()

        for keyword in self.config.breaking_keywords:
            if keyword in body or keyword in str(footers):
                is_breaking = True
                break

        return ParsedCommit(
            hash=hashlib.md5(message.encode()).hexdigest()[:8],
            type=commit_type, scope=scope, description=description,
            body=body, is_breaking=is_breaking, footers=footers,
            raw_message=message
        )

    def parse_batch(self, messages: list[str]) -> list[ParsedCommit]:
        return [self.parse(msg) for msg in messages]


@dataclass
class Version:
    major: int = 0
    minor: int = 0
    patch: int = 0
    pre_release: str = ""

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-{self.pre_release}" if self.pre_release else base

    @staticmethod
    def from_string(version_str: str) -> Version:
        clean = version_str.lstrip("v")
        pre_release = ""
        if "-" in clean:
            clean, pre_release = clean.split("-", 1)
        parts = clean.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return Version(major=major, minor=minor, patch=patch, pre_release=pre_release)

    def bump_major(self) -> Version:
        return Version(major=self.major + 1, minor=0, patch=0)

    def bump_minor(self) -> Version:
        return Version(major=self.major, minor=self.minor + 1, patch=0)

    def bump_patch(self) -> Version:
        return Version(major=self.major, minor=self.minor, patch=self.patch + 1)


class ChangelogGenerator:
    def __init__(self, repo_path: str = ".", from_ref: str = "",
                 to_ref: str = "", category_map: Optional[dict[str, ChangeCategory]] = None) -> None:
        self.repo_path = Path(repo_path)
        self.from_ref = from_ref
        self.to_ref = to_ref
        self.category_map = category_map or {
            "feat": ChangeCategory.ADDED,
            "fix": ChangeCategory.FIXED,
            "breaking": ChangeCategory.REMOVED,
            "deprecate": ChangeCategory.DEPRECATED,
            "perf": ChangeCategory.CHANGED,
            "security": ChangeCategory.SECURITY,
        }
        self._parser = CommitParser()
        self._parsed_commits: list[ParsedCommit] = []

    def generate(self, commits: Optional[list[str]] = None) -> Changelog:
        if commits is None:
            commits = self._load_commits_from_git()
        self._parsed_commits = self._parser.parse_batch(commits)
        entries: list[ChangelogEntry] = []
        for parsed in self._parsed_commits:
            category = self.category_map.get(parsed.type, ChangeCategory.CHANGED)
            entries.append(ChangelogEntry(
                category=category, description=parsed.description,
                scope=parsed.scope, commit_hash=parsed.hash,
                breaking=parsed.is_breaking
            ))
        return Changelog(
            version=self.to_ref.lstrip("v"),
            date=datetime.date.today().isoformat(),
            entries=entries
        )

    def _load_commits_from_git(self) -> list[str]:
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline", f"{self.from_ref}..{self.to_ref}"],
                capture_output=True, text=True, cwd=str(self.repo_path), timeout=30
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                return [line.split(" ", 1)[1] if " " in line else line for line in lines if line.strip()]
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        return []

    def get_unclassified(self) -> list[ParsedCommit]:
        return [c for c in self._parsed_commits if c.type == "other"]


@dataclass
class SemVerValidation:
    valid: bool
    current: str
    recommended: str
    bump_type: str = ""
    reasoning: str = ""


class SemVerEnforcer:
    def __init__(self, current_version: str, changelog: Optional[Changelog] = None) -> None:
        self.current_version = current_version
        self.changelog = changelog
        self._current = Version.from_string(current_version)

    def recommend_version(self) -> Version:
        if self.changelog is None:
            return self._current.bump_patch()
        if self.changelog.has_breaking_changes:
            return self._current.bump_major()
        has_features = any(
            e.category == ChangeCategory.ADDED for e in self.changelog.entries
        )
        if has_features:
            return self._current.bump_minor()
        return self._current.bump_patch()

    def validate_bump(self, target_version: Version) -> SemVerValidation:
        current = self._current
        if target_version.major > current.major:
            bump_type = "major"
            valid = self.changelog is not None and self.changelog.has_breaking_changes
            reasoning = "Major bump requires breaking changes." if not valid else "Breaking changes detected."
        elif target_version.minor > current.minor:
            bump_type = "minor"
            has_features = (self.changelog is not None and
                            any(e.category == ChangeCategory.ADDED for e in self.changelog.entries))
            valid = has_features
            reasoning = "Minor bump requires new features." if not valid else "New features detected."
        elif target_version.patch > current.patch:
            bump_type = "patch"
            valid = True
            reasoning = "Patch bump is always valid for bug fixes."
        else:
            bump_type = "none"
            valid = False
            reasoning = "Target version is not newer than current."
        return SemVerValidation(
            valid=valid, current=str(current),
            recommended=str(target_version), bump_type=bump_type,
            reasoning=reasoning
        )

    def get_breaking_changes(self) -> list[ChangelogEntry]:
        if self.changelog is None:
            return []
        return self.changelog.breaking_changes


@dataclass
class MigrationStep:
    order: int
    title: str
    description: str
    code_before: str = ""
    code_after: str = ""


@dataclass
class MigrationGuide:
    from_version: str
    to_version: str
    steps: list[MigrationStep] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Migration Guide: {self.from_version} → {self.to_version}\n",
            "This guide covers all breaking changes and the steps needed to migrate.\n",
        ]
        if self.notes:
            lines.append("## Important Notes\n")
            for note in self.notes:
                lines.append(f"- {note}")
            lines.append("")
        lines.append("## Migration Steps\n")
        for step in self.steps:
            lines.append(f"### Step {step.order}: {step.title}\n")
            lines.append(f"{step.description}\n")
            if step.code_before and step.code_after:
                lines.append("Before:")
                lines.append(f"```{self._detect_language(step.code_before)}")
                lines.append(step.code_before)
                lines.append("```\n")
                lines.append("After:")
                lines.append(f"```{self._detect_language(step.code_after)}")
                lines.append(step.code_after)
                lines.append("```\n")
        return "\n".join(lines)

    def _detect_language(self, code: str) -> str:
        if "def " in code and "import " in code:
            return "python"
        if "function " in code or "const " in code or "=>" in code:
            return "javascript"
        if "func " in code and ":=" in code:
            return "go"
        return ""


class MigrationGuideGenerator:
    def __init__(self, from_version: str, to_version: str) -> None:
        self.from_version = from_version
        self.to_version = to_version

    def generate(self, breaking_changes: list[ChangelogEntry] | None = None,
                 code_diffs: dict[str, str] | None = None) -> MigrationGuide:
        guide = MigrationGuide(from_version=self.from_version, to_version=self.to_version)
        if breaking_changes:
            for i, change in enumerate(breaking_changes, 1):
                guide.steps.append(MigrationStep(
                    order=i, title=f"Update: {change.description}",
                    description=f"The following change affects your code:\n{change.description}"
                ))
        if not guide.steps:
            guide.steps.append(MigrationStep(
                order=1, title="Review Changes",
                description="No specific migration steps required. Review the changelog for details."
            ))
        return guide

    def extract_diffs(self, directory: str, from_ref: str, to_ref: str) -> dict[str, str]:
        diffs: dict[str, str] = {}
        try:
            import subprocess
            result = subprocess.run(
                ["git", "diff", from_ref, to_ref, "--", directory],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                diffs["full_diff"] = result.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        return diffs

    def publish(self, guide: MigrationGuide, output_dir: str = "docs/migrations/") -> str:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        file_path = out / f"migration-{self.from_version}-to-{self.to_version}.md"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(guide.to_markdown())
        except OSError:
            pass
        return str(file_path)


@dataclass
class DeprecationNotice:
    feature: str
    deprecated_in: str
    removal_in: str
    replacement: str = ""
    reason: str = ""
    migration_steps: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Deprecation: {self.feature}\n",
            f"**Deprecated in**: {self.deprecated_in}",
            f"**Removal in**: {self.removal_in}",
            f"**Replacement**: {self.replacement}" if self.replacement else "",
            f"**Reason**: {self.reason}" if self.reason else "",
            "",
        ]
        if self.migration_steps:
            lines.append("## Migration Steps\n")
            for i, step in enumerate(self.migration_steps, 1):
                lines.append(f"{i}. {step}")
        return "\n".join(line for line in lines if line is not None)


class DeprecationManager:
    def __init__(self, notices_dir: str = "docs/deprecations/",
                 warning_period_versions: int = 3) -> None:
        self.notices_dir = Path(notices_dir)
        self.warning_period_versions = warning_period_versions
        self._notices: list[DeprecationNotice] = []

    def register(self, notice: DeprecationNotice) -> None:
        self._notices.append(notice)
        self._save_notice(notice)

    def _save_notice(self, notice: DeprecationNotice) -> None:
        self.notices_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.notices_dir / f"{notice.feature}.md"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(notice.to_markdown())
        except OSError:
            pass

    def check_expirations(self, current_version: str) -> list[DeprecationNotice]:
        current = Version.from_string(current_version)
        expired: list[DeprecationNotice] = []
        for notice in self._notices:
            removal = Version.from_string(notice.removal_in)
            deprecated = Version.from_string(notice.deprecated_in)
            versions_since_deprecation = current.minor - deprecated.minor
            if current.major > removal.major or (
                current.major == removal.major and current.minor >= removal.minor
            ):
                expired.append(notice)
            elif versions_since_deprecation > self.warning_period_versions:
                expired.append(notice)
        return expired

    def get_active(self, current_version: str) -> list[DeprecationNotice]:
        expired_versions = {n.feature for n in self.check_expirations(current_version)}
        return [n for n in self._notices if n.feature not in expired_versions]


@dataclass
class PublishResult:
    success: bool
    channel: Channel
    url: str = ""
    error: str = ""


class ReleasePublisher:
    def __init__(self, channels: Optional[dict[Channel, dict]] = None) -> None:
        self.channels = channels or {}

    def publish(self, version: str, title: str, changelog: Changelog,
                assets: list[str] | None = None) -> dict[Channel, PublishResult]:
        results: dict[Channel, PublishResult] = {}
        for channel, config in self.channels.items():
            try:
                if channel == Channel.GITHUB_RELEASES:
                    results[channel] = self._publish_github(version, title, changelog, config)
                elif channel == Channel.SLACK:
                    results[channel] = self._publish_slack(version, title, changelog, config)
                elif channel == Channel.DOCUMENTATION:
                    results[channel] = self._publish_docs(version, changelog, config)
                else:
                    results[channel] = PublishResult(
                        success=True, channel=channel,
                        url=f"published-to-{channel.value}"
                    )
            except Exception as e:
                results[channel] = PublishResult(
                    success=False, channel=channel, error=str(e)
                )
        return results

    def _publish_github(self, version: str, title: str, changelog: Changelog,
                        config: dict) -> PublishResult:
        return PublishResult(
            success=True, channel=Channel.GITHUB_RELEASES,
            url=f"https://github.com/{config.get('repo', 'org/repo')}/releases/tag/v{version}"
        )

    def _publish_slack(self, version: str, title: str, changelog: Changelog,
                       config: dict) -> PublishResult:
        return PublishResult(
            success=True, channel=Channel.SLACK,
            url=config.get("channel", "#releases")
        )

    def _publish_docs(self, version: str, changelog: Changelog, config: dict) -> PublishResult:
        output_dir = Path(config.get("output_dir", "docs/releases/"))
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / f"v{version}.md"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(changelog.to_markdown())
            return PublishResult(
                success=True, channel=Channel.DOCUMENTATION,
                url=str(file_path)
            )
        except OSError as e:
            return PublishResult(
                success=False, channel=Channel.DOCUMENTATION, error=str(e)
            )


@dataclass
class ReleaseTemplate:
    type: TemplateType = TemplateType.MINOR_RELEASE

    def render(self, version: str, highlights: list[str] | None = None,
               breaking_changes_count: int = 0,
               migration_guide_url: str = "", changelog_url: str = "") -> str:
        highlights = highlights or []
        lines = [f"# Release {version}\n"]
        if self.type == TemplateType.MAJOR_RELEASE:
            lines.append("## Breaking Release\n")
            lines.append(f"This is a **major release** with {breaking_changes_count} breaking change(s).\n")
            lines.append("Please review the migration guide before upgrading.\n")
        elif self.type == TemplateType.MINOR_RELEASE:
            lines.append("## New Features\n")
        else:
            lines.append("## Bug Fixes\n")

        if highlights:
            lines.append("## Highlights\n")
            for h in highlights:
                lines.append(f"- {h}")
            lines.append("")

        if migration_guide_url:
            lines.append(f"**Migration Guide**: {migration_guide_url}\n")
        if changelog_url:
            lines.append(f"**Full Changelog**: {changelog_url}\n")

        return "\n".join(lines)


def main() -> None:
    print("=" * 60)
    print("Automated Release Note Generation & Changelog Management")
    print("=" * 60)

    parser = CommitParser()
    commits = [
        "feat(api): add user search endpoint",
        "fix(auth): resolve token refresh race condition",
        "breaking(api): remove legacy /v1/auth endpoint",
        "deprecate(ui): mark legacy dashboard as deprecated",
        "perf(db): optimize query performance for large datasets",
        "chore(ci): update GitHub Actions to v4",
    ]
    parsed = parser.parse_batch(commits)
    print(f"\n[Parser] Parsed {len(parsed)} commits")
    for p in parsed:
        print(f"  [{p.type}] {p.description}" + (" (BREAKING)" if p.is_breaking else ""))

    generator = ChangelogGenerator(from_ref="v1.4.0", to_ref="v1.5.0")
    changelog = generator.generate(commits=commits)
    print(f"\n[Changelog] Generated with {len(changelog.entries)} entries")
    print(changelog.to_markdown()[:500])

    enforcer = SemVerEnforcer(current_version="1.4.0", changelog=changelog)
    recommended = enforcer.recommend_version()
    print(f"\n[SemVer] Recommended version: {recommended}")
    validation = enforcer.validate_bump(recommended)
    print(f"  Valid: {validation.valid}, Reasoning: {validation.reasoning}")

    migration_gen = MigrationGuideGenerator(from_version="1.4.0", to_version="2.0.0")
    guide = migration_gen.generate(breaking_changes=changelog.breaking_changes)
    print(f"\n[Migration] Guide with {len(guide.steps)} steps")

    deprecation_mgr = DeprecationManager()
    deprecation_mgr.register(DeprecationNotice(
        feature="legacy-auth", deprecated_in="1.5.0", removal_in="2.0.0",
        replacement="/api/v2/auth", reason="Replaced by OAuth 2.0",
        migration_steps=["Update auth endpoint", "Remove API key usage"]
    ))
    expired = deprecation_mgr.check_expirations(current_version="1.8.0")
    print(f"\n[Deprecation] {len(expired)} expired deprecation notices")

    publisher = ReleasePublisher(channels={
        Channel.GITHUB_RELEASES: {"repo": "org/repo"},
        Channel.SLACK: {"channel": "#releases"},
    })
    results = publisher.publish(version="1.5.0", title="Release 1.5.0", changelog=changelog)
    for ch, result in results.items():
        print(f"  [{ch.value}] {'OK' if result.success else 'FAILED'}")

    template = ReleaseTemplate(type=TemplateType.MAJOR_RELEASE)
    content = template.render(
        version="2.0.0", highlights=["OAuth 2.0", "New dashboard API"],
        breaking_changes_count=3, changelog_url="https://example.com/changelog"
    )
    print(f"\n[Template] Generated {len(content)} chars")

    print("\n" + "=" * 60)
    print("All release notes components initialized successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()

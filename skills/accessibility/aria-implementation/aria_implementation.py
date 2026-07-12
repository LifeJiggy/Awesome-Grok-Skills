"""
ARIA Implementation Module — Validation, anti-pattern detection, widget pattern templates,
and best practices for WAI-ARIA 1.2 accessible rich internet applications.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ARIARoleCategory(Enum):
    """Categories of ARIA roles per WAI-ARIA 1.2."""
    LANDMARK = "landmark"
    WIDGET = "widget"
    STRUCTURE = "structure"
    LIVE_REGION = "live_region"
    WINDOW = "window"
    COMPOSITE = "composite"
    SECTION = "section"
    SECTIONHEAD = "sectionhead"


class Severity(Enum):
    """Issue severity levels."""
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


class IssueType(Enum):
    """Types of ARIA issues."""
    REDUNDANT_ARIA = "redundant_aria"
    MISSING_REQUIRED = "missing_required"
    INVALID_ROLE = "invalid_role"
    INVALID_STATE = "invalid_state"
    MISSING_KEYBOARD = "missing_keyboard"
    HIDDEN_FOCUSABLE = "hidden_focusable"
    MISSING_LABEL = "missing_label"
    INCORRECT_PROPERTY = "incorrect_property"
    MISSING_SEMANTIC = "missing_semantic"
    FRAGILE_PATTERN = "fragile_pattern"


# ---------------------------------------------------------------------------
# ARIA role definitions
# ---------------------------------------------------------------------------

@dataclass
class ARIARoleDefinition:
    """Definition of an ARIA role with its requirements."""
    name: str
    category: ARIARoleCategory
    description: str
    required_states: List[str] = field(default_factory=list)
    required_properties: List[str] = field(default_factory=list)
    allowed_states: List[str] = field(default_factory=list)
    allowed_properties: List[str] = field(default_factory=list)
    html_equivalent: Optional[str] = None
    keyboard_interactions: Dict[str, str] = field(default_factory=dict)
    parent_roles: List[str] = field(default_factory=list)
    children_roles: List[str] = field(default_factory=list)
    deprecated: bool = False


# Well-known ARIA roles with their requirements
ARIA_ROLES: Dict[str, ARIARoleDefinition] = {
    "button": ARIARoleDefinition(
        name="button",
        category=ARIARoleCategory.WIDGET,
        description="An interactive element that triggers an action when activated",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-pressed", "aria-expanded", "aria-disabled"],
        allowed_properties=["aria-label", "aria-labelledby", "aria-describedby"],
        html_equivalent="<button>",
        keyboard_interactions={
            "Enter": "Activates the button",
            "Space": "Activates the button",
        },
    ),
    "tab": ARIARoleDefinition(
        name="tab",
        category=ARIARoleCategory.WIDGET,
        description="A grouping label for the contents of a tabpanel",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-selected", "aria-expanded", "aria-disabled"],
        allowed_properties=["aria-controls", "aria-labelledby"],
        parent_roles=["tablist"],
        keyboard_interactions={
            "Tab": "Move focus into the tablist",
            "ArrowRight": "Move to next tab",
            "ArrowLeft": "Move to previous tab",
            "Home": "Move to first tab",
            "End": "Move to last tab",
            "Enter/Space": "Activate the tab",
        },
    ),
    "tablist": ARIARoleDefinition(
        name="tablist",
        category=ARIARoleCategory.COMPOSITE,
        description="A list of tab elements",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-orientation"],
        allowed_properties=["aria-label", "aria-labelledby"],
        children_roles=["tab"],
    ),
    "tabpanel": ARIARoleDefinition(
        name="tabpanel",
        category=ARIARoleCategory.WIDGET,
        description="The container for content associated with a tab",
        required_states=[],
        required_properties=[],
        allowed_states=[],
        allowed_properties=["aria-labelledby", "aria-describedby"],
    ),
    "dialog": ARIARoleDefinition(
        name="dialog",
        category=ARIARoleCategory.WINDOW,
        description="A dialog window containing content",
        required_states=[],
        required_properties=[],
        allowed_states=[],
        allowed_properties=["aria-label", "aria-labelledby", "aria-describedby"],
        keyboard_interactions={
            "Escape": "Close the dialog",
            "Tab": "Move focus within the dialog (trapped)",
        },
    ),
    "alertdialog": ARIARoleDefinition(
        name="alertdialog",
        category=ARIARoleCategory.WINDOW,
        description="A dialog that contains an alert message",
        required_states=[],
        required_properties=[],
        allowed_states=[],
        allowed_properties=["aria-label", "aria-labelledby", "aria-describedby"],
    ),
    "combobox": ARIARoleDefinition(
        name="combobox",
        category=ARIARoleCategory.COMPOSITE,
        description="A composite widget with a text input and popup list",
        required_states=[],
        required_properties=["aria-expanded", "aria-controls"],
        allowed_states=["aria-activedescendant", "aria-autocomplete", "aria-required"],
        allowed_properties=["aria-label", "aria-labelledby", "aria-describedby"],
        keyboard_interactions={
            "ArrowDown": "Open or move to next option",
            "ArrowUp": "Move to previous option",
            "Enter": "Select current option",
            "Escape": "Close the popup",
        },
    ),
    "menu": ARIARoleDefinition(
        name="menu",
        category=ARIARoleCategory.COMPOSITE,
        description="A list of choices or actions",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-orientation"],
        allowed_properties=["aria-label", "aria-labelledby"],
        children_roles=["menuitem", "menuitemcheckbox", "menuitemradio"],
    ),
    "menuitem": ARIARoleDefinition(
        name="menuitem",
        category=ARIARoleCategory.WIDGET,
        description="An item in a menu",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-disabled", "aria-checked"],
        allowed_properties=["aria-label", "aria-labelledby"],
        parent_roles=["menu", "menubar", "group"],
    ),
    "grid": ARIARoleDefinition(
        name="grid",
        category=ARIARoleCategory.COMPOSITE,
        description="A grid with interactive cells",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-readonly", "aria-multiselectable", "aria-orientation"],
        allowed_properties=["aria-label", "aria-labelledby", "aria-describedby"],
        children_roles=["row", "rowgroup"],
    ),
    "tree": ARIARoleDefinition(
        name="tree",
        category=ARIARoleCategory.COMPOSITE,
        description="A hierarchical list where items can expand/collapse",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-multiselectable", "aria-orientation"],
        allowed_properties=["aria-label", "aria-labelledby"],
        children_roles=["treeitem"],
    ),
    "treeitem": ARIARoleDefinition(
        name="treeitem",
        category=ARIARoleCategory.WIDGET,
        description="An item in a tree view",
        required_states=[],
        required_properties=[],
        allowed_states=["aria-expanded", "aria-selected", "aria-disabled"],
        allowed_properties=["aria-level", "aria-setsize", "aria-posinset"],
        parent_roles=["tree", "group"],
    ),
    "slider": ARIARoleDefinition(
        name="slider",
        category=ARIARoleCategory.WIDGET,
        description="A range input where the user selects a value",
        required_states=[],
        required_properties=["aria-valuenow", "aria-valuemin", "aria-valuemax"],
        allowed_states=["aria-disabled", "aria-readonly", "aria-orientation"],
        allowed_properties=["aria-label", "aria-labelledby", "aria-valuetext"],
        keyboard_interactions={
            "ArrowRight/Up": "Increase value",
            "ArrowLeft/Down": "Decrease value",
            "Home": "Set to minimum",
            "End": "Set to maximum",
        },
    ),
    "progressbar": ARIARoleDefinition(
        name="progressbar",
        category=ARIARoleCategory.WIDGET,
        description="An element indicating progress of a task",
        required_states=[],
        required_properties=[],
        allowed_states=[],
        allowed_properties=["aria-valuenow", "aria-valuemin", "aria-valuemax", "aria-valuetext", "aria-label"],
    ),
    "banner": ARIARoleDefinition(
        name="banner",
        category=ARIARoleCategory.LANDMARK,
        description="Site-wide header content",
        html_equivalent="<header> (when not nested in article/section/nav/main)",
    ),
    "navigation": ARIARoleDefinition(
        name="navigation",
        category=ARIARoleCategory.LANDMARK,
        description="Navigation links region",
        html_equivalent="<nav>",
    ),
    "main": ARIARoleDefinition(
        name="main",
        category=ARIARoleCategory.LANDMARK,
        description="Main content of the document",
        html_equivalent="<main>",
    ),
    "contentinfo": ARIARoleDefinition(
        name="contentinfo",
        category=ARIARoleCategory.LANDMARK,
        description="Site-wide footer information",
        html_equivalent="<footer> (when not nested in article/section)",
    ),
    "region": ARIARoleDefinition(
        name="region",
        category=ARIARoleCategory.LANDMARK,
        description="A generic landmark region",
        html_equivalent="<section> with accessible name",
    ),
    "alert": ARIARoleDefinition(
        name="alert",
        category=ARIARoleCategory.LIVE_REGION,
        description="An important, usually time-sensitive message",
        allowed_states=["aria-atomic", "aria-relevant"],
    ),
    "status": ARIARoleDefinition(
        name="status",
        category=ARIARoleCategory.LIVE_REGION,
        description="A status update or advisory information",
        allowed_states=["aria-atomic", "aria-relevant"],
    ),
    "log": ARIARoleDefinition(
        name="log",
        category=ARIARoleCategory.LIVE_REGION,
        description="A sequential information update (chat, log, etc.)",
        allowed_states=["aria-atomic", "aria-relevant"],
    ),
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ARIAConfig:
    """Configuration for ARIA validation."""
    check_redundant: bool = True
    check_required: bool = True
    check_keyboard: bool = True
    check_hidden: bool = True
    check_labels: bool = True
    check_semantics: bool = True
    wcag_level: str = "AA"
    custom_rules: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ARIAIssue:
    """A single ARIA implementation issue."""
    rule: str
    message: str
    selector: str
    severity: Severity
    issue_type: IssueType
    fix_suggestion: str
    wcag_criteria: List[str] = field(default_factory=list)
    element_html: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "message": self.message,
            "selector": self.selector,
            "severity": self.severity.value,
            "issue_type": self.issue_type.value,
            "fix_suggestion": self.fix_suggestion,
            "wcag_criteria": self.wcag_criteria,
        }


@dataclass
class ValidationResult:
    """Aggregated validation results."""
    url: str
    issues: List[ARIAIssue] = field(default_factory=list)
    roles_found: List[str] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_issues(self) -> int:
        return len(self.issues)

    @property
    def by_severity(self) -> Dict[Severity, int]:
        counts: Dict[Severity, int] = {s: 0 for s in Severity}
        for issue in self.issues:
            counts[issue.severity] += 1
        return counts

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "total_issues": self.total_issues,
            "by_severity": {s.value: c for s, c in self.by_severity.items()},
            "roles_found": self.roles_found,
            "issues": [i.to_dict() for i in self.issues],
            "timestamp": self.timestamp,
        }


@dataclass
class WidgetPattern:
    """Complete widget pattern implementation template."""
    name: str
    description: str
    required_roles: List[str]
    required_properties: List[str]
    keyboard_interactions: Dict[str, str]
    html_template: str
    wcag_criteria: List[str] = field(default_factory=list)
    apg_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "required_roles": self.required_roles,
            "required_properties": self.required_properties,
            "keyboard_interactions": self.keyboard_interactions,
            "html_template": self.html_template,
        }


# ---------------------------------------------------------------------------
# Widget pattern library
# ---------------------------------------------------------------------------

WIDGET_PATTERNS: Dict[str, WidgetPattern] = {
    "tabs": WidgetPattern(
        name="Tabs",
        description="A tabbed interface with tab list, tabs, and tab panels",
        required_roles=["tablist", "tab", "tabpanel"],
        required_properties=["aria-controls", "aria-labelledby"],
        keyboard_interactions={
            "Tab": "Move focus into the tab list, then to the active tab panel",
            "ArrowRight": "Move to the next tab and activate it",
            "ArrowLeft": "Move to the previous tab and activate it",
            "Home": "Move to the first tab",
            "End": "Move to the last tab",
        },
        html_template="""<div class="tabs">
  <div role="tablist" aria-label="Sample tabs">
    <button role="tab" id="tab-1" aria-selected="true"
            aria-controls="panel-1" tabindex="0">Tab 1</button>
    <button role="tab" id="tab-2" aria-selected="false"
            aria-controls="panel-2" tabindex="-1">Tab 2</button>
    <button role="tab" id="tab-3" aria-selected="false"
            aria-controls="panel-3" tabindex="-1">Tab 3</button>
  </div>
  <div role="tabpanel" id="panel-1" aria-labelledby="tab-1" tabindex="0">
    Content for Tab 1
  </div>
  <div role="tabpanel" id="panel-2" aria-labelledby="tab-2" tabindex="0"
       hidden>Content for Tab 2</div>
  <div role="tabpanel" id="panel-3" aria-labelledby="tab-3" tabindex="0"
       hidden>Content for Tab 3</div>
</div>""",
        wcag_criteria=["4.1.2"],
    ),
    "accordion": WidgetPattern(
        name="Accordion",
        description="A vertically stacked set of expandable sections",
        required_roles=[],
        required_properties=["aria-expanded", "aria-controls"],
        keyboard_interactions={
            "Enter/Space": "Toggle the expanded state of the header",
            "ArrowDown": "Move focus to the next accordion header",
            "ArrowUp": "Move focus to the previous accordion header",
            "Home": "Move focus to the first accordion header",
            "End": "Move focus to the last accordion header",
        },
        html_template="""<div class="accordion">
  <h3>
    <button aria-expanded="true" aria-controls="section-1" id="header-1">
      Section 1
    </button>
  </h3>
  <div id="section-1" role="region" aria-labelledby="header-1">
    <p>Content for section 1</p>
  </div>
  <h3>
    <button aria-expanded="false" aria-controls="section-2" id="header-2">
      Section 2
    </button>
  </h3>
  <div id="section-2" role="region" aria-labelledby="header-2" hidden>
    <p>Content for section 2</p>
  </div>
</div>""",
        wcag_criteria=["4.1.2"],
    ),
    "combobox": WidgetPattern(
        name="Combobox",
        description="A text input with a popup list of options",
        required_roles=["combobox"],
        required_properties=["aria-expanded", "aria-controls", "aria-activedescendant"],
        keyboard_interactions={
            "ArrowDown": "Open the listbox or move to the next option",
            "ArrowUp": "Move to the previous option",
            "Enter": "Select the current option and close the listbox",
            "Escape": "Close the listbox without selecting",
            "Home": "Move to the first option",
            "End": "Move to the last option",
        },
        html_template="""<label for="combo-input">Choose a fruit:</label>
<div role="combobox" aria-expanded="false" aria-controls="combo-listbox">
  <input id="combo-input" type="text" aria-autocomplete="list"
         aria-activedescendant="" aria-labelledby="combo-label" />
</div>
<ul id="combo-listbox" role="listbox" aria-label="Fruits" hidden>
  <li role="option" id="opt-1" aria-selected="false">Apple</li>
  <li role="option" id="opt-2" aria-selected="false">Banana</li>
  <li role="option" id="opt-3" aria-selected="false">Cherry</li>
</ul>""",
        wcag_criteria=["4.1.2"],
    ),
    "modal-dialog": WidgetPattern(
        name="Modal Dialog",
        description="A modal dialog that traps focus and can be dismissed with Escape",
        required_roles=["dialog"],
        required_properties=["aria-label or aria-labelledby"],
        keyboard_interactions={
            "Escape": "Close the dialog",
            "Tab": "Move focus to the next focusable element within the dialog",
            "Shift+Tab": "Move focus to the previous focusable element within the dialog",
        },
        html_template="""<div role="dialog" aria-modal="true" aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  <button id="confirm-btn">Confirm</button>
  <button id="cancel-btn">Cancel</button>
</div>
<div class="overlay" aria-hidden="true"></div>""",
        wcag_criteria=["2.1.2", "4.1.2"],
    ),
    "tree-view": WidgetPattern(
        name="Tree View",
        description="A hierarchical list with expandable/collapsible items",
        required_roles=["tree", "treeitem"],
        required_properties=["aria-level", "aria-setsize", "aria-posinset"],
        keyboard_interactions={
            "ArrowDown": "Move to the next visible treeitem",
            "ArrowUp": "Move to the previous visible treeitem",
            "ArrowRight": "Expand the current node or move to first child",
            "ArrowLeft": "Collapse the current node or move to parent",
            "Home": "Move to the first treeitem",
            "End": "Move to the last visible treeitem",
            "Enter": "Activate the current treeitem",
        },
        html_template="""<ul role="tree" aria-label="File browser">
  <li role="treeitem" aria-expanded="true" aria-level="1">
    <span>Documents</span>
    <ul role="group">
      <li role="treeitem" aria-level="2">
        <span>report.pdf</span>
      </li>
      <li role="treeitem" aria-expanded="false" aria-level="2">
        <span>Images</span>
        <ul role="group">
          <li role="treeitem" aria-level="3"><span>photo.jpg</span></li>
        </ul>
      </li>
    </ul>
  </li>
</ul>""",
        wcag_criteria=["4.1.2"],
    ),
}


class WidgetPatternLibrary:
    """Library of WAI-ARIA widget pattern implementations."""

    def __init__(self) -> None:
        self._patterns = dict(WIDGET_PATTERNS)

    def get_pattern(self, name: str) -> Optional[WidgetPattern]:
        return self._patterns.get(name)

    def list_patterns(self) -> List[str]:
        return list(self._patterns.keys())

    def add_pattern(self, pattern: WidgetPattern) -> None:
        self._patterns[pattern.name.lower().replace(" ", "-")] = pattern


# ---------------------------------------------------------------------------
# Core validator
# ---------------------------------------------------------------------------

class ARIAValidator:
    """
    Validates ARIA implementation on web pages, detecting anti-patterns,
    missing required properties, redundant ARIA, and keyboard issues.
    """

    REDUNDANT_ARIA: Dict[str, List[str]] = {
        "button": ["role=\"button\""],
        "a[href]": ["role=\"link\""],
        "input[type='checkbox']": ["role=\"checkbox\""],
        "input[type='radio']": ["role=\"radio\""],
        "input[type='range']": ["role=\"slider\""],
        "select": ["role=\"listbox\""],
        "h1": ["role=\"heading\""],
        "h2": ["role=\"heading\""],
        "h3": ["role=\"heading\""],
        "h4": ["role=\"heading\""],
        "h5": ["role=\"heading\""],
        "h6": ["role=\"heading\""],
        "nav": ["role=\"navigation\""],
        "main": ["role=\"main\""],
        "header": ["role=\"banner\""],
        "footer": ["role=\"contentinfo\""],
        "table": ["role=\"table\""],
        "ul": ["role=\"list\""],
        "ol": ["role=\"list\""],
    }

    def __init__(self, config: Optional[ARIAConfig] = None):
        self.config = config or ARIAConfig()

    def validate_url(self, url: str) -> ValidationResult:
        """Validate ARIA on a page (production: DOM parsing + browser automation)."""
        result = ValidationResult(url=url)
        elements = self._extract_aria_elements(url)
        result.roles_found = list({e.get("role", "") for e in elements if e.get("role")})

        for elem in elements:
            issues = self._validate_element(elem)
            result.issues.extend(issues)

        return result

    def validate_component(self, html: str, pattern: Optional[str] = None) -> List[ARIAIssue]:
        """Validate ARIA on a component's HTML."""
        issues: List[ARIAIssue] = []
        elements = self._parse_html_elements(html)

        for elem in elements:
            issues.extend(self._validate_element(elem))

        if pattern:
            pattern_issues = self._validate_against_pattern(html, pattern)
            issues.extend(pattern_issues)

        return issues

    def _extract_aria_elements(self, url: str) -> List[Dict[str, Any]]:
        """Extract ARIA-related elements from a page."""
        return []

    def _parse_html_elements(self, html: str) -> List[Dict[str, Any]]:
        """Parse HTML and extract elements with ARIA attributes."""
        elements = []
        role_pattern = re.compile(r'role=["\'](\w+)["\']')
        aria_pattern = re.compile(r'aria-(\w+)=["\']([^"\']*)["\']')

        for match in role_pattern.finditer(html):
            role = match.group(1)
            aria_attrs = {}
            for aria_match in aria_pattern.finditer(html):
                aria_attrs[f"aria-{aria_match.group(1)}"] = aria_match.group(2)

            elements.append({
                "role": role,
                "aria_attributes": aria_attrs,
                "html": html[max(0, match.start() - 50):match.end() + 100],
                "tag": "div",
                "has_text_content": True,
                "has_keyboard_handler": False,
                "is_focusable": False,
            })

        return elements

    def _validate_element(self, element: Dict[str, Any]) -> List[ARIAIssue]:
        """Validate a single element's ARIA usage."""
        issues: List[ARIAIssue] = []
        role = element.get("role", "")
        aria = element.get("aria_attributes", {})
        selector = element.get("selector", "unknown")

        if self.config.check_redundant:
            redundant = self._check_redundant(element)
            issues.extend(redundant)

        if self.config.check_required and role in ARIA_ROLES:
            missing = self._check_required_properties(role, aria, selector)
            issues.extend(missing)

        if self.config.check_hidden:
            hidden_issues = self._check_hidden_focusable(element, aria, selector)
            issues.extend(hidden_issues)

        if self.config.check_labels:
            label_issues = self._check_labeling(role, aria, selector)
            issues.extend(label_issues)

        if self.config.check_keyboard and role in ARIA_ROLES:
            kb_issues = self._check_keyboard_support(element, role, selector)
            issues.extend(kb_issues)

        return issues

    def _check_redundant(self, element: Dict[str, Any]) -> List[ARIAIssue]:
        """Check for redundant ARIA on native HTML elements."""
        issues = []
        role = element.get("role", "")
        tag = element.get("tag", "")

        for native_tag, redundant_roles in self.REDUNDANT_ARIA.items():
            if tag == native_tag or (tag.startswith(native_tag)):
                for redundant in redundant_roles:
                    if role in redundant:
                        issues.append(
                            ARIAIssue(
                                rule="redundant-aria",
                                message=f"Redundant role='{role}' on <{tag}> — native element already conveys this semantics",
                                selector=element.get("selector", ""),
                                severity=Severity.MINOR,
                                issue_type=IssueType.REDUNDANT_ARIA,
                                fix_suggestion=f"Remove role=\"{role}\" from <{tag}>",
                                wcag_criteria=["4.1.2"],
                            )
                        )
        return issues

    def _check_required_properties(
        self, role: str, aria: Dict[str, str], selector: str
    ) -> List[ARIAIssue]:
        """Check that required ARIA properties are present."""
        issues = []
        role_def = ARIA_ROLES.get(role)
        if not role_def:
            return issues

        for prop in role_def.required_properties:
            if prop not in aria:
                issues.append(
                    ARIAIssue(
                        rule="missing-required-property",
                        message=f"Role '{role}' requires {prop} but it is not present",
                        selector=selector,
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.MISSING_REQUIRED,
                        fix_suggestion=f"Add {prop}=\"...\" to the element with role=\"{role}\"",
                        wcag_criteria=["4.1.2"],
                    )
                )
        return issues

    def _check_hidden_focusable(
        self, element: Dict[str, Any], aria: Dict[str, str], selector: str
    ) -> List[ARIAIssue]:
        """Check that hidden elements are not focusable."""
        issues = []
        if aria.get("aria-hidden") == "true":
            if element.get("is_focusable") or element.get("tabindex", 0) >= 0:
                issues.append(
                    ARIAIssue(
                        rule="hidden-focusable",
                        message="Element with aria-hidden='true' is focusable — this creates an invisible focus target",
                        selector=selector,
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.HIDDEN_FOCUSABLE,
                        fix_suggestion="Remove tabindex or make the element not focusable, or remove aria-hidden",
                        wcag_criteria=["4.1.2"],
                    )
                )
        return issues

    def _check_labeling(
        self, role: str, aria: Dict[str, str], selector: str
    ) -> List[ARIAIssue]:
        """Check that interactive roles have accessible names."""
        issues = []
        interactive_roles = {"button", "link", "tab", "menuitem", "combobox", "slider", "dialog"}
        if role in interactive_roles:
            has_label = any(k in aria for k in ["aria-label", "aria-labelledby"])
            has_text = element.get("has_text_content", False) if isinstance(element, dict) else False
            if not has_label and not has_text:
                issues.append(
                    ARIAIssue(
                        rule="missing-label",
                        message=f"Interactive role '{role}' has no accessible name (no aria-label, aria-labelledby, or visible text)",
                        selector=selector,
                        severity=Severity.SERIOUS,
                        issue_type=IssueType.MISSING_LABEL,
                        fix_suggestion="Add aria-label or visible text content to provide an accessible name",
                        wcag_criteria=["4.1.2", "1.1.1"],
                    )
                )
        return issues

    def _check_keyboard_support(
        self, element: Dict[str, Any], role: str, selector: str
    ) -> List[ARIAIssue]:
        """Check that interactive roles have keyboard support."""
        issues = []
        role_def = ARIA_ROLES.get(role)
        if not role_def or not role_def.keyboard_interactions:
            return issues

        if not element.get("has_keyboard_handler", False):
            issues.append(
                ARIAIssue(
                    rule="missing-keyboard",
                    message=f"Role '{role}' requires keyboard interactions but no keyboard handler detected",
                    selector=selector,
                    severity=Severity.CRITICAL,
                    issue_type=IssueType.MISSING_KEYBOARD,
                    fix_suggestion=f"Implement keyboard handlers: {', '.join(role_def.keyboard_interactions.keys())}",
                    wcag_criteria=["2.1.1", "4.1.2"],
                )
            )
        return issues

    def _validate_against_pattern(self, html: str, pattern_name: str) -> List[ARIAIssue]:
        """Validate HTML against a specific widget pattern."""
        issues = []
        pattern = WIDGET_PATTERNS.get(pattern_name)
        if not pattern:
            issues.append(
                ARIAIssue(
                    rule="unknown-pattern",
                    message=f"Unknown widget pattern: {pattern_name}",
                    selector="",
                    severity=Severity.MINOR,
                    issue_type=IssueType.INCORRECT_PROPERTY,
                    fix_suggestion=f"Valid patterns: {', '.join(WIDGET_PATTERNS.keys())}",
                )
            )
            return issues

        for role in pattern.required_roles:
            if f'role="{role}"' not in html:
                issues.append(
                    ARIAIssue(
                        rule="missing-pattern-role",
                        message=f"Widget pattern '{pattern_name}' requires role='{role}' but it was not found",
                        selector="",
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.MISSING_REQUIRED,
                        fix_suggestion=f"Add role=\"{role}\" to the appropriate element",
                    )
                )
        return issues


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the ARIA implementation validator and pattern library."""
    print("ARIA Implementation Validator")
    print("=" * 60)

    # Validate a component
    validator = ARIAValidator()
    component = '''
    <div role="tablist">
      <div role="tab" aria-selected="true">Tab 1</div>
      <div role="tab" aria-selected="false">Tab 2</div>
    </div>
    <div role="tabpanel">Content 1</div>
    <div role="tabpanel">Content 2</div>
    '''
    issues = validator.validate_component(component, pattern="tabs")
    print(f"\nComponent validation: {len(issues)} issues")
    for issue in issues:
        print(f"  [{issue.severity.value}] {issue.message}")
        print(f"    Fix: {issue.fix_suggestion}")

    # Widget pattern library
    print("\n\nWidget Pattern Library")
    print("=" * 60)
    lib = WidgetPatternLibrary()
    for name in lib.list_patterns():
        pattern = lib.get_pattern(name)
        print(f"\n  {pattern.name}: {pattern.description}")
        print(f"    Required roles: {pattern.required_roles}")
        print(f"    Keyboard: {', '.join(pattern.keyboard_interactions.keys())}")

    # Tab pattern details
    tabs = lib.get_pattern("tabs")
    if tabs:
        print(f"\n\nTabs Pattern HTML Template:")
        print(tabs.html_template)


if __name__ == "__main__":
    main()

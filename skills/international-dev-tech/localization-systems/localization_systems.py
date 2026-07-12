"""
Localization Systems Module
Software localization and internationalization tools
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TextDirection(Enum):
    LTR = "ltr"
    RTL = "rtl"

class DateFormat(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    FULL = "full"

class PluralCategory(Enum):
    ZERO = "zero"
    ONE = "one"
    TWO = "two"
    FEW = "few"
    MANY = "many"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TranslationEntry:
    """Single translation entry."""
    key: str
    value: str
    locale: str
    context: str = ""
    description: str = ""
    plural_forms: Dict[str, str] = field(default_factory=dict)

@dataclass
class LocaleInfo:
    """Locale configuration."""
    code: str
    name: str
    language: str
    region: str
    direction: TextDirection = TextDirection.LTR
    decimal_separator: str = "."
    thousands_separator: str = ","
    currency_symbol: str = "$"
    currency_code: str = "USD"
    date_format: str = "YYYY-MM-DD"
    time_format: str = "HH:mm:ss"

@dataclass
class FormattingResult:
    """Result of locale formatting."""
    original_value: Any
    formatted_value: str
    locale: str
    format_type: str


# ---------------------------------------------------------------------------
# Locale Database
# ---------------------------------------------------------------------------

LOCALES: Dict[str, LocaleInfo] = {
    "en-US": LocaleInfo("en-US", "English (US)", "en", "US", TextDirection.LTR, ".", ",", "$", "USD", "MM/DD/YYYY"),
    "en-GB": LocaleInfo("en-GB", "English (UK)", "en", "GB", TextDirection.LTR, ".", ",", "£", "GBP", "DD/MM/YYYY"),
    "es-ES": LocaleInfo("es-ES", "Spanish (Spain)", "es", "ES", TextDirection.LTR, ",", ".", "€", "EUR", "DD/MM/YYYY"),
    "fr-FR": LocaleInfo("fr-FR", "French (France)", "fr", "FR", TextDirection.LTR, ",", " ", "€", "EUR", "DD/MM/YYYY"),
    "de-DE": LocaleInfo("de-DE", "German (Germany)", "de", "DE", TextDirection.LTR, ",", ".", "€", "EUR", "DD.MM.YYYY"),
    "ja-JP": LocaleInfo("ja-JP", "Japanese (Japan)", "ja", "JP", TextDirection.LTR, ".", ",", "¥", "JPY", "YYYY/MM/DD"),
    "ar-SA": LocaleInfo("ar-SA", "Arabic (Saudi Arabia)", "ar", "SA", TextDirection.RTL, "٫", "٬", "ر.س", "SAR", "DD/MM/YYYY"),
    "he-IL": LocaleInfo("he-IL", "Hebrew (Israel)", "he", "IL", TextDirection.RTL, ".", ",", "₪", "ILS", "DD/MM/YYYY"),
    "zh-CN": LocaleInfo("zh-CN", "Chinese (Simplified)", "zh", "CN", TextDirection.LTR, ".", ",", "¥", "CNY", "YYYY-MM-DD"),
    "pt-BR": LocaleInfo("pt-BR", "Portuguese (Brazil)", "pt", "BR", TextDirection.LTR, ",", ".", "R$", "BRL", "DD/MM/YYYY"),
}


# ---------------------------------------------------------------------------
# Localization Manager
# ---------------------------------------------------------------------------

class LocalizationManager:
    """Manages translations and locale settings."""

    def __init__(self, default_locale: str = "en-US") -> None:
        self.default_locale = default_locale
        self._translations: Dict[str, Dict[str, TranslationEntry]] = {}

    def add_translation(self, locale: str, key: str, value: str, context: str = "") -> None:
        if locale not in self._translations:
            self._translations[locale] = {}
        self._translations[locale][key] = TranslationEntry(key=key, value=value, locale=locale, context=context)

    def add_plural_translation(self, locale: str, key: str, forms: Dict[str, str]) -> None:
        if locale not in self._translations:
            self._translations[locale] = {}
        self._translations[locale][key] = TranslationEntry(
            key=key, value=forms.get("other", ""), locale=locale, plural_forms=forms
        )

    def translate(self, key: str, locale: str = "", variables: Optional[Dict[str, Any]] = None) -> str:
        locale = locale or self.default_locale
        translations = self._translations.get(locale, {})
        entry = translations.get(key)
        if entry is None:
            entry = self._translations.get(self.default_locale, {}).get(key)
        if entry is None:
            return f"[{key}]"
        value = entry.value
        if variables:
            for k, v in variables.items():
                value = value.replace("{" + k + "}", str(v))
        return value

    def translate_plural(self, key: str, count: int, locale: str = "", variables: Optional[Dict[str, Any]] = None) -> str:
        locale = locale or self.default_locale
        translations = self._translations.get(locale, {})
        entry = translations.get(key)
        if entry is None or not entry.plural_forms:
            return self.translate(key, locale, variables)
        form = PluralizationRules.get_form(locale, count)
        value = entry.plural_forms.get(form, entry.plural_forms.get("other", ""))
        if variables:
            variables["count"] = count
            for k, v in variables.items():
                value = value.replace("{" + k + "}", str(v))
        return value

    def get_available_locales(self) -> List[str]:
        return list(self._translations.keys())

    def get_missing_translations(self, target_locale: str) -> List[str]:
        source_keys = set(self._translations.get(self.default_locale, {}).keys())
        target_keys = set(self._translations.get(target_locale, {}).keys())
        return list(source_keys - target_keys)


# ---------------------------------------------------------------------------
# Pluralization Rules
# ---------------------------------------------------------------------------

class PluralizationRules:
    """CLDR-based pluralization rules."""

    @staticmethod
    def get_form(locale: str, count: int) -> str:
        lang = locale.split("-")[0]
        if lang in ("en", "de", "nl", "it", "pt", "es"):
            return "one" if count == 1 else "other"
        elif lang == "fr":
            return "one" if count in (0, 1) else "other"
        elif lang == "ru":
            if count % 10 == 1 and count % 100 != 11:
                return "one"
            elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
                return "few"
            elif count % 10 == 0 or (5 <= count % 10 <= 9) or (11 <= count % 100 <= 14):
                return "many"
            return "other"
        elif lang == "ar":
            if count == 0:
                return "zero"
            elif count == 1:
                return "one"
            elif count == 2:
                return "two"
            elif count % 100 >= 3 and count % 100 <= 10:
                return "few"
            elif count % 100 >= 11 and count % 100 <= 99:
                return "many"
            return "other"
        elif lang == "ja":
            return "other"
        elif lang == "zh":
            return "other"
        return "other"

    @staticmethod
    def get_forms(locale: str, count: int) -> List[str]:
        lang = locale.split("-")[0]
        if lang in ("en", "de"):
            return ["one", "other"] if count == 1 else ["other"]
        elif lang == "ru":
            return ["one", "few", "many", "other"]
        elif lang == "ar":
            return ["zero", "one", "two", "few", "many", "other"]
        return ["other"]


# ---------------------------------------------------------------------------
# Locale Formatter
# ---------------------------------------------------------------------------

class LocaleFormatter:
    """Formats dates, numbers, and currency by locale."""

    def __init__(self) -> None:
        self._locale_cache: Dict[str, LocaleInfo] = LOCALES.copy()

    def get_locale(self, locale_code: str) -> Optional[LocaleInfo]:
        return self._locale_cache.get(locale_code)

    def format_date(self, date_str: str, locale: str = "en-US", format_type: DateFormat = DateFormat.LONG) -> str:
        locale_info = self._locale_cache.get(locale, self._locale_cache["en-US"])
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.now()

        if format_type == DateFormat.SHORT:
            return dt.strftime("%m/%d/%Y" if locale_info.region == "US" else "%d/%m/%Y")
        elif format_type == DateFormat.LONG:
            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
            return f"{months[dt.month - 1]} {dt.day}, {dt.year}"
        return dt.strftime(locale_info.date_format)

    def format_currency(self, amount: float, locale: str = "en-US", currency: str = "USD") -> str:
        locale_info = self._locale_cache.get(locale, self._locale_cache["en-US"])
        formatted = f"{amount:,.2f}"
        if locale_info.decimal_separator == ",":
            formatted = formatted.replace(".", "DEC").replace(",", locale_info.thousands_separator).replace("DEC", locale_info.decimal_separator)
        return f"{locale_info.currency_symbol}{formatted}"

    def format_number(self, value: float, locale: str = "en-US", decimal_places: int = 2) -> str:
        locale_info = self._locale_cache.get(locale, self._locale_cache["en-US"])
        formatted = f"{value:,.{decimal_places}f}"
        if locale_info.decimal_separator == ",":
            formatted = formatted.replace(".", "DEC").replace(",", locale_info.thousands_separator).replace("DEC", locale_info.decimal_separator)
        return formatted


# ---------------------------------------------------------------------------
# Layout Detector
# ---------------------------------------------------------------------------

class LayoutDetector:
    """Detects text direction and layout requirements."""

    RTL_LOCALES = {"ar", "he", "fa", "ur", "yi", "ps", "sd", "ug"}

    def is_rtl(self, locale: str) -> bool:
        lang = locale.split("-")[0]
        return lang in self.RTL_LOCALES

    def get_direction(self, locale: str) -> TextDirection:
        return TextDirection.RTL if self.is_rtl(locale) else TextDirection.LTR

    def get_mirror_selectors(self, locale: str) -> Dict[str, str]:
        if not self.is_rtl(locale):
            return {}
        return {
            "margin-left": "margin-right",
            "margin-right": "margin-left",
            "padding-left": "padding-right",
            "padding-right": "padding-left",
            "float: left": "float: right",
            "float: right": "float: left",
            "text-align: left": "text-align: right",
            "text-align: right": "text-align: left",
        }


# ---------------------------------------------------------------------------
# Pseudo-Localization
# ---------------------------------------------------------------------------

class PseudoLocalizer:
    """Generates pseudo-localized strings for testing."""

    CHARS = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"}

    def pseudo_localize(self, text: str) -> str:
        result = ""
        for char in text:
            if char.isalpha() and char in self.CHARS:
                result += self.CHARS[char]
            else:
                result += char
        return f"[{result}]"

    def expand_text(self, text: str, expansion_factor: float = 1.3) -> str:
        target_len = int(len(text) * expansion_factor)
        padding = target_len - len(text)
        return text + "!" * padding


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Localization Systems module."""
    print("=" * 60)
    print("  Localization Systems Module — Demo")
    print("=" * 60)

    # Manager
    manager = LocalizationManager(default_locale="en-US")
    manager.add_translation("en-US", "welcome", "Welcome, {name}!")
    manager.add_translation("es-ES", "welcome", "¡Bienvenido, {name}!")
    manager.add_translation("ja-JP", "welcome", "ようこそ、{name}さん！")
    manager.add_translation("fr-FR", "welcome", "Bienvenue, {name} !")

    message = manager.translate("welcome", "es-ES", {"name": "Carlos"})
    print(f"\n[+] Translation: {message}")

    # Pluralization
    print(f"\n[+] Plural Forms:")
    for count in [0, 1, 2, 5, 25]:
        form = PluralizationRules.get_form("en", count)
        print(f"    EN count={count}: {form}")

    # Formatting
    formatter = LocaleFormatter()
    print(f"\n[+] Date Formatting:")
    print(f"    EN-US: {formatter.format_date('2024-01-15T14:30:00Z', 'en-US')}")
    print(f"    DE-DE: {formatter.format_date('2024-01-15T14:30:00Z', 'de-DE')}")

    print(f"\n[+] Currency Formatting:")
    print(f"    EN-US: {formatter.format_currency(1234.56, 'en-US')}")
    print(f"    JA-JP: {formatter.format_currency(123456, 'ja-JP')}")
    print(f"    DE-DE: {formatter.format_currency(1234.56, 'de-DE')}")

    # RTL
    detector = LayoutDetector()
    print(f"\n[+] RTL Detection:")
    print(f"    ar-SA: {detector.is_rtl('ar-SA')}")
    print(f"    he-IL: {detector.is_rtl('he-IL')}")
    print(f"    en-US: {detector.is_rtl('en-US')}")

    # Pseudo-localization
    pseudo = PseudoLocalizer()
    print(f"\n[+] Pseudo-Localization:")
    print(f"    Original: 'Hello World'")
    print(f"    Pseudo: {pseudo.pseudo_localize('Hello World')}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

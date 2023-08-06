from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, DefaultDict

from better_translation._babel.lazy_proxy import LazyProxy
from better_translation.types import (
    Locale,
    RawPlural,
    RawSingular,
    TranslatedPlural,
    TranslatedSingular,
    TranslatedText,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from better_translation.translator import ITranslator


class ITextProvider(ABC):
    """Text provider interface."""

    _translators_mapping: Mapping[Locale, ITranslator]
    """Mapping of locales to translators."""

    @abstractmethod
    def gettext(
        self,
        raw_singular: str | RawSingular,
        locale: Locale | None = None,
    ) -> TranslatedSingular:
        """Get text.

        :param raw_singular: Singular form of the text.
        :param plural: Plural form of the text.
        :param n: Number of items to determine the plural form.
        :param locale: Locale to use for translation.
        :return: Translated text.
        """

    @abstractmethod
    def ngettext(
        self,
        raw_singular: str | RawSingular,
        raw_plural: str | RawPlural,
        n: int,
        locale: Locale | None = None,
    ) -> TranslatedPlural:
        """Get text.

        :param raw_singular: Singular form of the text.
        :param raw_plural: Plural form of the text.
        :param n: Number of items to determine the plural form.
        :param locale: Locale to use for translation.
        :return: Translated text.
        """

    @abstractmethod
    def lazy_gettext(
        self,
        raw_singular: str | RawSingular,
        locale: Locale | None = None,
    ) -> LazyProxy:
        """Get text lazy.

        :param raw_singular: Singular form of the text.
        :param locale: Locale to use for translation.
        :return: LazyProxy to translated text.
        """


@dataclass(slots=True)
class TextProvider(ITextProvider):
    _translators_mapping: DefaultDict[Locale, ITranslator]
    _locale_getter: Callable[[], Locale] = lambda: Locale("en")  # noqa: E731

    def _gettext(
        self,
        raw_singular: str | RawSingular,
        raw_plural: str | RawPlural | None = None,
        n: int = 1,
        locale: Locale | None = None,
    ) -> TranslatedText:
        if locale is None:
            locale = self._locale_getter()

        translator = self._translators_mapping[locale]
        return translator.translate(
            locale=locale,
            raw_singular=raw_singular,  # type: ignore[arg-type]
            raw_plural=raw_plural,  # type: ignore[arg-type]
            n=n,
        )

    def gettext(
        self,
        raw_singular: str | RawSingular,
        locale: Locale | None = None,
    ) -> TranslatedSingular:
        return self._gettext(  # type: ignore[return-value]
            raw_singular=raw_singular,
            locale=locale,
        )

    def ngettext(
        self,
        raw_singular: str | RawSingular,
        raw_plural: str | RawPlural,
        n: int,
        locale: Locale | None = None,
    ) -> TranslatedPlural:
        return self._gettext(  # type: ignore[return-value]
            raw_singular=raw_singular,
            raw_plural=raw_plural,
            n=n,
            locale=locale,
        )

    def lazy_gettext(
        self,
        raw_singular: str | RawSingular,
        locale: Locale | None = None,
    ) -> LazyProxy:
        return LazyProxy(
            self.gettext,
            raw_singular=raw_singular,
            locale=locale,
        )

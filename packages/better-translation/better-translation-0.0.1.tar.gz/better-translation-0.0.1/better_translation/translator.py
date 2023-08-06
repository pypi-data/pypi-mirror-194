from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, cast

from better_translation.types import (
    RawPlural,
    RawSingular,
    TranslatedPlural,
    TranslatedSingular,
    TranslatedText,
)

if TYPE_CHECKING:
    from better_translation.types import Locale


class ITranslator(ABC):
    @abstractmethod
    def translate(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None = None,
        n: int = 1,
    ) -> TranslatedText:
        ...


class DefaultTranslator(ITranslator):
    def translate(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None = None,
        n: int = 1,
    ) -> TranslatedText:
        if raw_plural is None:
            return self._translate_singular(locale, raw_singular)

        return self._translate_plural(
            locale,
            raw_singular,
            raw_plural,
            n,
        )

    def _translate_singular(
        self,
        locale: Locale,  # noqa: ARG002
        raw_singular: RawSingular,
    ) -> TranslatedSingular:
        return cast(TranslatedSingular, raw_singular)

    def _translate_plural(
        self,
        locale: Locale,  # noqa: ARG002
        raw_singular: RawSingular,
        raw_plural: RawPlural,
        n: int,
    ) -> TranslatedPlural:
        return cast(
            TranslatedPlural,
            raw_singular if n == 1 else raw_plural,
        )

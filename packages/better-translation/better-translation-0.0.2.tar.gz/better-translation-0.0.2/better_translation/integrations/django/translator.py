from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from better_translation.cache import ICache, InMemoryCache
from better_translation.integrations.django.models import (
    BaseMessage,
    BaseTranslation,
)
from better_translation.translator import ITranslator

if TYPE_CHECKING:
    from better_translation.types import (
        Locale,
        RawPlural,
        RawSingular,
        TranslatedText,
    )

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class DjangoTranslator(ITranslator):
    message_model: type[BaseMessage]
    translations_cache: ICache[BaseTranslation | None] = field(
        default_factory=InMemoryCache[BaseTranslation | None],
    )

    def translate(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None = None,
        n: int = 1,
    ) -> TranslatedText:
        translation = self._get_translation(raw_singular, locale)

        if raw_plural:
            return self._translate_plural(
                raw_singular,
                raw_plural,
                n,
                translation,
            )

        return self._translate_singular(
            raw_singular,
            translation,
        )  # type: ignore[return-value]

    def _translate_singular(
        self,
        raw_singular: RawSingular,
        translation: BaseTranslation | None,
    ) -> str:
        return translation.singular if translation else raw_singular

    def _translate_plural(
        self,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None,
        n: int,
        translation: BaseTranslation | None,
    ) -> TranslatedText:
        if translation:
            singular = translation.singular
            plural = translation.plural
        else:
            singular = raw_singular
            plural = raw_plural

        if plural:
            return plural if n != 1 else singular  # type: ignore[return-value]

        return singular  # type: ignore[return-value]

    def _get_message(self, raw_singular: RawSingular) -> BaseMessage:
        logger.debug("Getting message %s", raw_singular)
        message, _ = self.message_model.objects.get_or_create(
            raw_singular=raw_singular,
        )

        return message

    def _get_translation(
        self,
        raw_singular: RawSingular,
        locale: Locale,
    ) -> BaseTranslation | None:
        cached_translation = self.translations_cache.get(
            raw_singular,
            locale,
        )

        if cached_translation:
            logger.debug(
                "Returning translation %s from cache",
                cached_translation,
            )
            return cached_translation

        logger.debug("Getting translation for %s", raw_singular)

        message = self._get_message(raw_singular)
        translation = message.translations.filter(
            locale=locale,
        ).first()

        self.translations_cache.set(
            translation,
            raw_singular,
            locale,
        )

        return translation

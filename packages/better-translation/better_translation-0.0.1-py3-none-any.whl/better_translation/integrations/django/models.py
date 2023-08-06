from __future__ import annotations

from typing import cast
from uuid import uuid4

try:
    from django.db import models
except ImportError as e:
    msg = "Django is not installed. To use Django integration, install Django."
    raise ValueError(msg) from e


MAX_MESSAGE_LENGTH = 4096


class DefaultLocalesChoices(models.TextChoices):
    RU = "ru", "Russian"
    EN = "en", "English"


class BaseMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    raw_singular = models.CharField(
        max_length=MAX_MESSAGE_LENGTH,
        verbose_name="Raw singular form of the message",
        unique=True,
    )

    raw_plural = models.CharField(
        max_length=MAX_MESSAGE_LENGTH,
        verbose_name="Raw plural form of the message",
        default="",
    )

    is_used = models.BooleanField(
        verbose_name="Is used",
        default=True,
    )

    translations: models.QuerySet[BaseTranslation]
    """A QuerySet of translations for this message."""

    def __str__(self) -> str:
        return f"Message: {self.raw_singular}"

    class _Meta:
        abstract = True

    Meta = cast("type[models.Model.Meta]", _Meta)


class BaseTranslation(models.Model):
    locale = models.CharField(
        max_length=5,
        verbose_name="Locale",
        choices=DefaultLocalesChoices.choices,
    )
    singular = models.TextField(
        verbose_name="Singular form of the text",
    )
    plural = models.TextField(
        verbose_name="Plural form of the text",
        default="",
        blank=True,
    )

    message = models.ForeignKey(
        BaseMessage,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    def __str__(self) -> str:
        return f"MessageTranslation({self.locale})"

    class _Meta:
        abstract = True

    Meta = cast("type[models.Model.Meta]", _Meta)

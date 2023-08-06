from __future__ import annotations

from django.contrib import admin

from better_translation.integrations.django.models import (
    BaseMessage,
    BaseTranslation,
)

admin.ModelAdmin.__class_getitem__ = classmethod(  # type: ignore[assignment]
    lambda cls, _: cls,
)
admin.TabularInline.__class_getitem__ = classmethod(  # type: ignore[assignment]
    lambda cls, _: cls,
)


class BaseMessageAdmin(admin.ModelAdmin[BaseMessage]):
    list_display = ("raw_singular", "is_used")
    readonly_fields = ("raw_singular", "raw_plural", "is_used")
    search_fields = (
        "raw_singular",
        "raw_plural",
        "translations__singular",
        "translations__plural",
    )


class BaseTranslationInline(admin.TabularInline[BaseTranslation]):
    extra = 0

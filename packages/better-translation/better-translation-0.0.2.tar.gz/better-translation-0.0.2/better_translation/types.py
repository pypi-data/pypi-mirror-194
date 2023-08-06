from __future__ import annotations

from typing import NewType

Locale = NewType("Locale", str)

RawText = NewType("RawText", str)
RawSingular = NewType("RawSingular", RawText)
RawPlural = NewType("RawPlural", RawText)

TranslatedText = NewType("TranslatedText", str)
TranslatedSingular = NewType("TranslatedSingular", TranslatedText)
TranslatedPlural = NewType("TranslatedPlural", TranslatedText)

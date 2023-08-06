from __future__ import annotations

import logging
from contextlib import suppress
from typing import TYPE_CHECKING

from better_translation._babel.extractor import extract_from_dir

if TYPE_CHECKING:
    from better_translation.integrations.django.models import BaseMessage


logger = logging.getLogger(__name__)


def update_messages(
    base_dir: str,
    message_model: type[BaseMessage],
) -> None:
    """Update messages in database.

    :param base_dir: Base directory for search.
    :param message_model: Message model.
    """
    already_saved_messages = message_model.objects.all()
    already_saved_messages_by_raw_singular = {
        message.raw_singular: message for message in already_saved_messages
    }
    already_saved_messages_by_raw_plural = {
        message.raw_plural: message for message in already_saved_messages
    }
    unused_message_ids = {message.id for message in already_saved_messages}

    messages_to_save: list[BaseMessage] = []
    messages_to_update: list[BaseMessage] = []

    extracted_messages = extract_from_dir(base_dir)

    for extracted_message in extracted_messages:
        logger.debug("Extracted message: %s", extracted_message)
        _filename, _lineno, messages, _comments, _context = extracted_message

        if isinstance(messages, str):
            raw_singular, raw_plural = messages, ""
        else:
            raw_singular, raw_plural = messages

        already_saved_message = already_saved_messages_by_raw_singular.get(
            raw_singular,
        ) or already_saved_messages_by_raw_plural.get(raw_plural)

        if already_saved_message is None:
            logger.info("New message: %s", raw_singular)
            message = message_model(
                raw_singular=raw_singular,
                raw_plural=raw_plural,
            )
            messages_to_save.append(message)
        else:
            logger.debug("Existing message: %s", already_saved_message)

            message_to_update = message_model(
                id=already_saved_message.id,
                raw_singular=raw_singular,
                raw_plural=raw_plural,
            )

            with suppress(KeyError):
                unused_message_ids.remove(already_saved_message.id)

            if not already_saved_message.is_used:
                message_to_update.is_used = True

            if (
                message_to_update.raw_singular
                != already_saved_message.raw_singular
                or message_to_update.raw_plural
                != already_saved_message.raw_plural
                or message_to_update.is_used != already_saved_message.is_used
            ):
                logger.info("Message to update: %s", message_to_update)
                messages_to_update.append(message_to_update)

    logger.info("Messages to save: %s", messages_to_save)
    logger.info("Messages to update: %s", messages_to_update)

    message_model.objects.bulk_create(messages_to_save)
    message_model.objects.bulk_update(
        messages_to_update,
        ["raw_singular", "raw_plural", "is_used"],
    )

    message_model.objects.filter(id__in=unused_message_ids).update(
        is_used=False,
    )

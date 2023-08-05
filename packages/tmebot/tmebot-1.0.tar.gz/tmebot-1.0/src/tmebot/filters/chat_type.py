from typing import Set, Optional, Union

from tapp import filters
from tbot_api import types


class ChatTypeFilter(filters.Filter):
    def __init__(
        self,
        chat_type: Union[str, Set[str]]
    ) -> None:
        self.chat_type = {chat_type} if isinstance(chat_type, str) else chat_type

    def find_chat_type(
        self,
        update: Union[
            types.Message,
            types.InlineQuery,
            types.CallbackQuery,
            types.ChatMemberUpdated,
            types.ChatJoinRequest
        ]
    ) -> Optional[str]:
        if isinstance(update, types.InlineQuery):
            chat_type = update.chat_type
        elif isinstance(update, types.CallbackQuery):
            chat_type = update.message.chat.type if update.message is not None else None
        elif isinstance(update, types.Message) or isinstance(update, types.ChatMemberUpdated) or isinstance(update, types.ChatJoinRequest):
            chat_type = update.chat.type
        else:
            chat_type = "unknown"

        return chat_type

    async def __call__(
        self, update: Union[
            types.Message,
            types.InlineQuery,
            types.CallbackQuery,
            types.ChatMemberUpdated,
            types.ChatJoinRequest
        ]
    ) -> bool:
        return self.find_chat_type(update) in self.chat_type

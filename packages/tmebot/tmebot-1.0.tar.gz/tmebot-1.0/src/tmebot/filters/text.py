from operator import contains as contains_operator
from typing import Any, Dict, Optional, Union

from tapp import filters
from tbot_api import types


class Text(filters.Filter):
    def __init__(
        self,
        text: Optional[str] = None,
        *,
        contains: Optional[str] = None,
        startswith: Optional[str] = None,
        endswith: Optional[str] = None,
        ignore_case: bool = False,
    ) -> None:
        self.text = text
        self.contains = contains
        self.startswith = startswith
        self.endswith = endswith
        self.ignore_case = ignore_case

        self.validate()

    def validate(self) -> None:
        if self.text and any({self.contains, self.startswith, self.endswith}):
            raise ValueError("You cannot use `text` parameter with another parameters!")

    def find_text(
        self, event: Union[types.Message, types.CallbackQuery, types.InlineQuery, types.Poll]
    ) -> Optional[str]:
        if isinstance(event, types.Message):
            text = event.text or event.caption
            if text is None:
                text = event.poll.question
        elif isinstance(event, types.CallbackQuery):
            text = event.data
        elif isinstance(event, types.InlineQuery):
            text = event.query
        elif isinstance(event, types.Poll):
            text = event.question
        else:
            annotation = self.find_text.__annotations__.get("event", "unannotated")  # noqa
            raise TypeError(
                "Type usage: %s - not allowed, allowed: %s." % (type(event), annotation)
            )

        return self.prepare_text(text=text)

    def prepare_text(
        self, text: Optional[str]
    ) -> Optional[str]:
        if text and self.ignore_case:
            return text.lower()
        return text

    async def __call__(
        self, event: Union[types.Message, types.CallbackQuery, types.InlineQuery, types.Poll]
    ) -> Union[bool, Dict[str, Any]]:
        text = self.find_text(event)
        if text is None:
            return False
        filter = True
        if self.text:
            filter &= text in self.prepare_text(self.text)
        if self.contains:
            filter &= contains_operator(text, self.prepare_text(self.contains))
        if self.startswith:
            filter &= text.startswith(self.prepare_text(self.startswith))
        if self.endswith:
            filter &= text.endswith(self.prepare_text(self.endswith))
        return filter

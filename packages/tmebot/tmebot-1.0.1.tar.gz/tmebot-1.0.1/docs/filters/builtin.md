Filters for message text and chat filtering are also available by default.

## ChatType

Telegram has these types of chat:
  + `sender`
  + `private`
  + `group`
  + `supergroup`
  + `channel`

This filter implements all types of chats.

```python
from tmebot import filters

filters.ChatType(chat_type={"group"})
filters.ChatType(chat_type="group")
filters.ChatType(chat_type={"group", "supergroup"})
filters.ChatType(chat_type=("group", "supergroup",))
filters.ChatType(chat_type=["group", "supergroup"])
```

## Text

Using this filter, you can filter the text by the presence 
of an insertion of a line, by the presence of a line, 
the line begins with, the line ends with, ignore the case.

```python
from tmebot import filters

filters.Text(text="Hello")

try:
    filters.Text(text="Text passed", contains="and contains passed not allowed")
except ValueError as e:
    print(e)

filters.Text(contains="contains hello", startswith="and startswith hello", endswith="and endswith also allowed")
```

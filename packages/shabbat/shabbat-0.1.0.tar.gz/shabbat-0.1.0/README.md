# is shabbat

## a simple module to save the shabbat in your code!


**example of a telegram bot:**
___
```python3
"""
an example of telegram bot that will not work in shabbat!
"""

from pyrogram import Client, filters, types
from shabbat import Shabbat


app = Client("my_account")
s = Shabbat()


@app.on_message(filters.incoming)
def shabbat_handler(_, m: types.Message):
    if s.is_shabbat():
        return m.reply_text("Today is Shabbat! send me your messages after that!")


app.run()
```

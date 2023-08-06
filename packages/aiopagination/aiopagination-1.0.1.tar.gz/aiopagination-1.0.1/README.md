# aiopagination
### About
`aiopagination` is a library written using the aiogram library to help you create pagination using inline buttons

**Info:** A sample to use
```python
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import types

# aiopagination library
from aiopagination.keyboards import base_cd, pagination_cd
from aiopagination.pagination import Pagination



storage = MemoryStorage()
API_TOKEN = env.str("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)



sample_list = [
    (1, "Apple", 'red'),
    (2, "Cucumber", "green"),
    (3, "Melon", "yellow"),
    (4, "Cherry", "red"),
    (5, "Watermelon", "green"),
    (6, "Banana", "yellow"),
    (7, "Carrot", "orange"),
    (8, "Kiwi", "green"),
    (9, "Malina", "red"),
    (10, "Apelsin", "yellow"),
    (11, "Lemon", "yellow"),
    (12, "Grape", "black"),
    (13, "Carrot", "red"),
    (14, "Potato", "yellow")
]


@dp.callback_query_handler(base_cd.filter())
async def show_item(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    item = callback_data.get("item")
    get_item = sample_list(item)
    text = f"Your selected <b>{get_item[0]}</b>"
    await call.message.answer(text)




@dp.callback_query_handler(pagination_cd.filter())
async def show_pagination(call: types.CallbackQuery, callback_data: dict):
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    max_pages = int(callback_data.get("max_pages"))
    action = callback_data.get("action")

    pagination = Pagination(items=sample_list)
    if action == "prev":
        await pagination.prev(call=call, start=start, end=end, max_pages=max_pages)
    elif action == "next":
        await pagination.next(call=call, start=start, end=end, max_pages=max_pages)
    else:
        await call.answer(cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```
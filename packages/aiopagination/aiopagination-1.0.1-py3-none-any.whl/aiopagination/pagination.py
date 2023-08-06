from typing import List
from aiogram import types

from keyboards import items_keyboard





class Pagination:
    def __init__(self, items: List):
        self.__items = items

    async def collect_data(self, start: int, end: int):
        i = 1
        text = ""
        for item in self.__items[start:end]:
            text += f"<b>{i})</b> {item[1]} - {item[2]}\n"
            i += 1
        return text

    async def prev(self, start, end, max_pages, call: types.CallbackQuery):
        if start == 0 and start - 10 <= 0:
            await call.answer("Bu birinchi sahifa", cache_time=1)
        elif max_pages - end < 10 and max_pages - end >= 0:  # 27 20
            new_start = start - 10
            new_end = start
            msg = await self.collect_data(start=new_start, end=new_end)
            markup = items_keyboard(start=new_start, end=new_end)
            await call.message.edit_text(msg, reply_markup=markup)
        else:
            msg = await self.collect_data(start=start - 10, end=end - 10)
            markup = items_keyboard(start=start - 10, end=end - 10)
            await call.message.edit_text(msg, reply_markup=markup)

    async def next(self, call: types.CallbackQuery, start, end, max_pages):
        if max_pages - end < 10 and max_pages - end > 0:
            msg = await self.collect_data(start=end, end=max_pages)
            markup = items_keyboard(start=end, end=max_pages)
            await call.message.edit_text(msg, reply_markup=markup)
        elif max_pages - end <= 0:
            await call.answer("Bu so'nggi sahifa", show_alert=True, cache_time=1)
        else:
            msg = await self.collect_data(start=start + 10, end=end + 10)
            markup = items_keyboard(start=start + 10, end=end + 10)
            await call.message.edit_text(msg, reply_markup=markup)
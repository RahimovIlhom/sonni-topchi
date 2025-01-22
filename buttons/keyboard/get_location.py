from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import json_manager


async def location_keyboard(chat_lang: str) -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        KeyboardButton(
            text=await json_manager.get_message(chat_lang, "send_location"),
            request_location=True
        ),
    )
    return keyboard_builder.as_markup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

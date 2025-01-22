from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import LANGUAGES
from loader import json_manager


async def languages_keyboard() -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    for lang_code in LANGUAGES:
        keyboard_builder.row(
            KeyboardButton(text=await json_manager.get_message(lang_code, "language_title")),
        )
    return keyboard_builder.as_markup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

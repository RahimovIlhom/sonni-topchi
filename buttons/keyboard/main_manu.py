from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import json_manager


async def main_menu_keyboard(chat_lang: str) -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "main_menu_button1")),
    )
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "main_menu_button2")),
    )
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "main_menu_button3")),
    )
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "main_menu_button4")),
    )
    return keyboard_builder.as_markup(resize_keyboard=True, row_width=1)

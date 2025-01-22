from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from loader import json_manager


async def robot_game_keyboard(chat_lang: str) -> ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "true_robot_number_button")),
    )
    keyboard_builder.row(
        KeyboardButton(text=await json_manager.get_message(chat_lang, "big_robot_number_button")),
        KeyboardButton(text=await json_manager.get_message(chat_lang, "small_robot_number_button")),
    )
    return keyboard_builder.as_markup(resize_keyboard=True, row_width=2, one_time_keyboard=True)

from aiogram.types import Message

from buttons.keyboard import main_menu_keyboard
from data import LANGUAGES
from filters import PrivateFilter
from loader import json_manager, dp, db


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.BACK_BUTTON)
async def settings(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'menu'),
        reply_markup=await main_menu_keyboard(user.get("chat_lang", LANGUAGES[1]))
    )

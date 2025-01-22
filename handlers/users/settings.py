import asyncio

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.keyboard import settings_keyboard, languages_keyboard, main_menu_keyboard
from data import LANGUAGES
from filters import PrivateFilter
from loader import json_manager, dp, db
from states import SetLanguageStates


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.MAIN_MENU_BUTTON4)
async def settings(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'settings_menu'),
        reply_markup=await settings_keyboard(user.get("chat_lang", LANGUAGES[1]))
    )


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.SET_LANGUAGE_BUTTON)
async def set_language(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'set_language'),
        reply_markup=await languages_keyboard()
    )
    await state.set_state(SetLanguageStates.language)
    await state.update_data(user=user)


@dp.message(SetLanguageStates.language, lambda msg: msg.text in json_manager.LANGUAGES_TITLES)
async def select_language(message: Message, state: FSMContext):
    lang = await json_manager.get_language_code(message.text)
    await message.answer(
        text=await json_manager.get_message(lang, 'set_language_completed'),
        reply_markup=await settings_keyboard(lang)
    )
    await state.clear()
    await db.user_update_chat_lang(message.from_user.id, lang)


@dp.message(StateFilter(SetLanguageStates))
async def error_value(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    warning_msg = await message.answer(
        text=await json_manager.get_message(data['user']['chat_lang'], 'warning')
    )
    await asyncio.sleep(3)
    await warning_msg.delete()

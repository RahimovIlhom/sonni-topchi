import asyncio
import random
from datetime import datetime, timezone

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from buttons.keyboard import ready_game_keyboard, main_menu_keyboard
from data import LANGUAGES
from filters import PrivateFilter
from loader import dp, json_manager, db
from states import FindNumberStates


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.MAIN_MENU_BUTTON1)
async def are_you_ready_game(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'are_you_ready_game'),
        reply_markup=await ready_game_keyboard(user.get("chat_lang", LANGUAGES[1]))
    )


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.READY_GAME_BUTTON)
async def find_number_start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'find_number_start'),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FindNumberStates.game)
    await state.update_data(robot_number=random.randrange(1, 101), user=user, created_at=datetime.now(timezone.utc))


@dp.message(FindNumberStates.game, F.text.regexp(r"^(100|[1-9][0-9]?)$"))
async def send_user_number(message: Message, state: FSMContext):
    user_num = int(message.text)
    data = await state.get_data()

    attempts = data.get('attempts', 0) + 1
    await state.update_data(attempts=attempts)

    robot_number = data.get('robot_number')
    user_lang = data['user']['chat_lang']

    if user_num == robot_number:
        await message.reply(
            text=(await json_manager.get_message(user_lang, key='find_number_complete')).format(attempts=attempts),
            reply_markup=await main_menu_keyboard(user_lang)
        )
        await state.clear()
        data.update({
            'attempts': attempts,
            'completed_at': datetime.now(timezone.utc)
        })
        await db.add_result(**data)
    else:
        hint_key = 'find_number_small' if user_num < robot_number else 'find_number_big'
        await message.reply(
            text=(await json_manager.get_message(user_lang, key=hint_key)).format(user_number=user_num)
        )


@dp.message(FindNumberStates.game)
async def error_value(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    warning_msg = await message.answer(
        text=await json_manager.get_message(data['user']['chat_lang'], 'find_number_error_value')
    )
    await asyncio.sleep(3)
    await warning_msg.delete()

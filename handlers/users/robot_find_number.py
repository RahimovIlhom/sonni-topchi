import asyncio
import random

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.keyboard import ready_robot_game_keyboard, robot_game_keyboard, main_menu_keyboard
from data import LANGUAGES
from filters import PrivateFilter
from loader import json_manager, dp, db
from states import RobotFindNumberStates


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.MAIN_MENU_BUTTON2)
async def robot_find_number(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(
        text=await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'robot_find_number'),
        reply_markup=await ready_robot_game_keyboard(user.get("chat_lang", LANGUAGES[1]))
    )


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.READY_ROBOT_GAME_BUTTON)
async def robot_find_number_start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    robot_number = random.randrange(1, 101)
    await state.set_state(RobotFindNumberStates.game)
    await state.update_data(min=1, max=101, robot_number=robot_number, user=user, attempts=1)
    await message.reply(
        text=(await json_manager.get_message(user.get("chat_lang", LANGUAGES[1]), 'get_robot_find_number')).format(
            robot_number=robot_number
        ),
        reply_markup=await robot_game_keyboard(user.get("chat_lang"))
    )


@dp.message(RobotFindNumberStates.game, lambda msg: msg.text in json_manager.TRUE_ROBOT_NUMBER_BUTTON)
async def truth_robot_number(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.reply(
        text=(await json_manager.get_message(data['user']['chat_lang'], 'congrats_robot_text')).format(
            attempts=data['attempts']
        ) + f"\n{await json_manager.get_message(data['user']['chat_lang'], 'menu')}",
        reply_markup=await main_menu_keyboard(data['user']['chat_lang'])
    )
    await state.clear()


@dp.message(RobotFindNumberStates.game, lambda msg: msg.text in json_manager.SMALL_ROBOT_NUMBER_BUTTON + json_manager.BIG_ROBOT_NUMBER_BUTTON)
async def handle_robot_button(message: Message, state: FSMContext):
    data = await state.get_data()
    robot_number = data.get('robot_number')
    user_lang = data['user']['chat_lang']
    attempts = data.get('attempts', 0) + 1

    if message.text in json_manager.SMALL_ROBOT_NUMBER_BUTTON:
        min_value = robot_number + 1
        max_value = data.get('max')
    else:
        min_value = data.get('min')
        max_value = robot_number

    if min_value >= max_value:
        await message.reply(
            text=await json_manager.get_message(user_lang, 'you_lost_text') + f"\n{await json_manager.get_message(data['user']['chat_lang'], 'menu')}",
            reply_markup=await main_menu_keyboard(user_lang)
        )
        await state.clear()
        return

    robot_number = random.randrange(min_value, max_value)
    await state.update_data(min=min_value, max=max_value, robot_number=robot_number, attempts=attempts)

    await message.reply(
        text=(await json_manager.get_message(user_lang, 'get_robot_find_number')).format(
            robot_number=robot_number
        ),
        reply_markup=await robot_game_keyboard(user_lang)
    )


@dp.message(StateFilter(RobotFindNumberStates))
async def error_message(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    warning_msg = await message.answer(
        text=await json_manager.get_message(data['user']['chat_lang'], 'robot_game_error')
    )
    await asyncio.sleep(2)
    await warning_msg.delete()

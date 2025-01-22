from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.keyboard import languages_keyboard, get_fullname_keyboard, get_contact_keyboard, location_keyboard, \
    main_menu_keyboard
from data import LANGUAGES
from filters import PrivateFilter
from loader import dp, db, json_manager
from states import RegisterStates
from utils import get_address


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        await message.answer(
            text=await json_manager.get_message(user.get("chat_lang"), 'menu'),
        )
        await state.clear()
    else:
        lang = message.from_user.language_code if message.from_user.language_code in LANGUAGES else "uz"
        await message.answer(
            text=await json_manager.get_message(lang, 'welcome'),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=await languages_keyboard()
        )
        await state.set_state(RegisterStates.chat_lang)


@dp.message(RegisterStates.chat_lang, lambda msg: msg.text in json_manager.LANGUAGES_TITLES)
async def set_chat_lang(message: Message, state: FSMContext):
    lang = await json_manager.get_language_code(message.text)
    await state.update_data(chat_lang=lang, tg_id=message.from_user.id, username=message.from_user.username)
    await message.answer(
        text=await json_manager.get_message(lang, 'get_fullname'),
        reply_markup=await get_fullname_keyboard(message.from_user.full_name)
    )
    await state.set_state(RegisterStates.fullname)


@dp.message(RegisterStates.fullname, lambda msg: msg.text)
async def set_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(fullname=message.text)
    await message.answer(
        text=await json_manager.get_message(data.get('chat_lang'), 'get_contact'),
        reply_markup=await get_contact_keyboard(data.get('chat_lang'))
    )
    await state.set_state(RegisterStates.phone)


@dp.message(RegisterStates.phone, lambda msg: msg.content_type == ContentType.CONTACT)
async def set_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        text=await json_manager.get_message(data.get('chat_lang'), 'get_location'),
        reply_markup=await location_keyboard(data.get('chat_lang'))
    )
    await state.set_state(RegisterStates.location)


@dp.message(RegisterStates.location, lambda msg: msg.content_type == ContentType.LOCATION)
async def set_location(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        text=await json_manager.get_message(data.get('chat_lang'), 'register_completed') +
             f"\n{await json_manager.get_message(data.get('chat_lang'), 'menu')}",
        reply_markup=await main_menu_keyboard(data.get('chat_lang'))
    )
    await state.clear()

    address = get_address(message.location.latitude, message.location.longitude, data.get('chat_lang'))
    data.update({
        'latitude': message.location.latitude,
        'longitude': message.location.longitude,
        'address': address
    })
    await db.add_user(**data)

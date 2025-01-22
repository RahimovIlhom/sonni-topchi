from aiogram.types import Message

from data import LANGUAGES
from filters import PrivateFilter
from loader import json_manager, dp, db


@dp.message(PrivateFilter(), lambda msg: msg.text in json_manager.MAIN_MENU_BUTTON3)
async def general_statistics(message: Message):
    results = await db.get_general_statistics()
    user = await db.get_user(message.from_user.id)
    lang = user.get("chat_lang", LANGUAGES[1])

    if not results:
        await message.answer(
            text=await json_manager.get_message(lang, 'no_statistics')
        )
        return

    # Statistikani formatlash
    formatted_results = f"<b>{message.text}</b>:\n\n"
    for i, result in enumerate(results, start=1):
        formatted_results += (await json_manager.get_message(lang, 'statistics_format')).format(
            index=i,
            fullname=result['fullname'],
            number_of_attempts=result['number_of_attempts'],
            time_taken=float(result['time_taken'])
        )

    # Javobni yuborish
    await message.answer(
        text=formatted_results,
        parse_mode="HTML",
    )

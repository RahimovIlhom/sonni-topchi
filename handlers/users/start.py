from aiogram.filters import CommandStart
from aiogram.types import Message

from filters import PrivateFilter
from loader import dp


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: Message):
    await message.answer("Assalomu aleykum")

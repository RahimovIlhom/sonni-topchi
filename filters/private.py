from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class PrivateFilter(BaseFilter):

    async def __call__(self, update: [Message, CallbackQuery], *args, **kwargs):
        chat = update.chat or update.message.chat
        return chat.type == 'private'
